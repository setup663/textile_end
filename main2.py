import sys
import logging
import configparser
from PyQt6 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pymysql
from texti import Ui_Form

logging.basicConfig(level=logging.INFO)

class DatabaseManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config2.ini')
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.config.get('Database', 'host'),
                user=self.config.get('Database', 'user'),
                password=self.config.get('Database', 'password'),
                database=self.config.get('Database', 'database'),
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            logging.error(f"Connection error: {str(e)}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Query error: {str(e)}")
            raise

class CuttingMapsContainer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(20)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QHBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def clear_maps(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_cutting_map(self, canvas):
        container = QtWidgets.QWidget()
        container.setFixedSize(600, 400)
        layout = QtWidgets.QVBoxLayout(container)
        layout.addWidget(canvas)
        self.scroll_layout.addWidget(container)

class Main(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.db_manager = DatabaseManager()
        self.current_order = None

        self.scrollAreaWidgetContents_2.setLayout(QtWidgets.QVBoxLayout())

        self.cutting_maps_container = CuttingMapsContainer()
        self.scrollAreaWidgetContents_2.layout().addWidget(self.cutting_maps_container)

        self.init_ui()
        self.load_orders()

    def init_ui(self):
        self.pushButton_calculate_rascr.clicked.connect(self.calculate_cutting)
        self.pushButton_back.clicked.connect(self.show_order_page)
        self.adjust_text_sizes()

    def adjust_text_sizes(self):
        for label in [self.label_2, self.label_3, self.label_4,
                      self.label_5, self.label_rascr, self.label_6]:
            label.adjustSize()

    def load_orders(self):
        try:
            with self.db_manager as db:
                query = """
                SELECT o.id, o.status,
                       c.organization_name, e.last_name as manager
                FROM order_request o
                LEFT JOIN customer c ON o.customer_id = c.id
                LEFT JOIN employee e ON o.employee_id = e.id
                WHERE o.status = 'В обработке'
                GROUP BY o.id, c.organization_name, e.last_name, o.status
                """
                orders = db.execute_query(query)

                for i in reversed(range(self.verticalLayout_2.count())):
                    self.verticalLayout_2.itemAt(i).widget().deleteLater()

                for order in orders:
                    btn_text = (f"Заказ #{order['id']} | {order['organization_name']} | "
                                f"Статус: {order['status']}")
                    btn = QtWidgets.QPushButton(btn_text)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f8f9fa;
                            border: 1px solid #dee2e6;
                            padding: 10px;
                            text-align: left;
                        }
                        QPushButton:hover { background-color: #e2e6ea; }
                    """)
                    btn.clicked.connect(lambda _, o=order: self.show_order_info(o))
                    self.verticalLayout_2.addWidget(btn)
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки заказов: {str(e)}")

    def show_order_info(self, order):
        try:
            self.current_order = order
            with self.db_manager as db:
                # Получаем доступные материалы для заказа
                fabric_query = """
                SELECT pm.supply_composition_id, pm.quantity, sc.width, sc.length, m.name as material_name, mt.name as material_type
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
                INNER JOIN material_type mt ON m.material_type_id = mt.id
                INNER JOIN order_composition oc ON pm.order_composition_id = oc.id
                WHERE oc.order_id = %s
                """
                fabric_data = db.execute_query(fabric_query, (order['id'],))

                # Группируем материалы по supply_composition_id
                fabrics = {}
                for fabric in fabric_data:
                    fabric_id = fabric['supply_composition_id']
                    if fabric_id not in fabrics:
                        fabrics[fabric_id] = {
                            'width': float(fabric['width']),
                            'height': float(fabric['length']),
                            'quantity': int(fabric['quantity']),
                            'material_name': fabric['material_name'],
                            'material_type': fabric['material_type']
                    }
                    else:
                        fabrics[fabric_id]['quantity'] += int(fabric['quantity'])

                # Отображаем доступные материалы
                fabric_info = "\n".join([
                    f"{data['material_name']} ({data['material_type']}) #{fabric_id}: {data['width']}x{data['height']} см, {data['quantity']} шт"
                    for fabric_id, data in fabrics.items()
                ])
                self.label_3.setText(f"Доступные материалы:\n{fabric_info}")
                self.label_3.adjustSize()

                # Получаем изделия в заказе
                order_query = """
                SELECT oc.id, p.name, oc.quantity, oc.width, oc.length, m.name as material_name, mt.name as material_type
                FROM order_composition oc
                JOIN product p ON oc.product_id = p.id
                JOIN product_materials pm ON oc.id = pm.order_composition_id
                JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                JOIN material m ON sc.material_id = m.id
                JOIN material_type mt ON m.material_type_id = mt.id
                WHERE oc.order_id = %s
                """
                order_items = db.execute_query(order_query, (order['id'],))

                total_products = sum(item['quantity'] for item in order_items)
                self.label_2.setText(f"Требуется изделий: {total_products}")
                self.label_2.adjustSize()

                total_area = sum(item['width'] * item['length'] * item['quantity']
                             for item in order_items if item['material_type'] == 'Ткань')
                self.label_5.setText(f"Общая площадь ткани: {total_area} см²")
                self.label_5.adjustSize()

        except Exception as e:
            self.show_error_message(f"Ошибка загрузки данных: {str(e)}")

    def calculate_cutting(self):
        if not self.current_order:
            return

        try:
            self.cutting_maps_container.clear_maps()

            with self.db_manager as db:
                # Получаем доступные материалы для заказа вместе с их названиями
                fabric_query = """
                SELECT pm.supply_composition_id, pm.quantity, sc.width, sc.length, m.name as material_name, mt.name as material_type
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
                INNER JOIN material_type mt ON m.material_type_id = mt.id
                INNER JOIN order_composition oc ON pm.order_composition_id = oc.id
                WHERE oc.order_id = %s
                """
                fabric_data = db.execute_query(fabric_query, (self.current_order['id'],))

                # Группируем материалы по supply_composition_id
                fabrics = {}
                for fabric in fabric_data:
                    fabric_id = fabric['supply_composition_id']
                    if fabric_id not in fabrics:
                        fabrics[fabric_id] = {
                            'width': float(fabric['width']),
                            'height': float(fabric['length']),
                            'quantity': int(fabric['quantity']),
                            'material_name': fabric['material_name'],
                            'material_type': fabric['material_type']
                    }
                    else:
                        fabrics[fabric_id]['quantity'] += int(fabric['quantity'])

                # Получаем изделия в заказе
                order_query = """
                SELECT oc.id, p.name, oc.quantity, oc.width, oc.length, m.name as material_name, mt.name as material_type
                FROM order_composition oc
                JOIN product p ON oc.product_id = p.id
                JOIN product_materials pm ON oc.id = pm.order_composition_id
                JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                JOIN material m ON sc.material_id = m.id
                JOIN material_type mt ON m.material_type_id = mt.id
                WHERE oc.order_id = %s
                """
                order_items = db.execute_query(order_query, (self.current_order['id'],))

                # Группируем изделия по материалам
                items_by_material = {}
                for item in order_items:
                    material_name = item['material_name']
                    material_type = item['material_type']
                    if material_name not in items_by_material:
                        items_by_material[material_name] = []
                    items_by_material[material_name].append({
                        'name': item['name'],
                        'width': float(item['width']),
                        'height': float(item['length']),
                        'quantity': int(item['quantity']),
                        'material_type': material_type
                    })

                # Выполняем расчет раскроя для каждого типа ткани
                for fabric_id, fabric in fabrics.items():
                    fabric_width = fabric['width']
                    fabric_height = fabric['height']
                    fabric_count = fabric['quantity']
                    material_name = fabric['material_name']
                    material_type = fabric['material_type']

                    if material_type == 'Ткань':
                        # Получаем изделия для данного материала
                        items = items_by_material.get(material_name, [])

                        for _ in range(fabric_count):
                            if all(item['quantity'] <= 0 for item in items):
                                break

                            # Выбираем изделия, которые можно разместить на этом полотне
                            valid_items = [item for item in items if item['quantity'] > 0]
                            placements, used = self.pack_single_fabric(
                                fabric_width,
                                fabric_height,
                                valid_items
                            )

                            if placements:
                                self.create_cutting_map(
                                    fabric_id,
                                    fabric_width,
                                    fabric_height,
                                    placements,
                                    material_name
                                )

                                # Уменьшаем количество оставшихся изделий
                                for u in used:
                                    for item in items:
                                        if item['name'] == u['name']:
                                            item['quantity'] -= u['count']
                                            break

                # Отображаем результаты
                result_text = "Результаты производства:\n"
                for material_name, items in items_by_material.items():
                    for item in items:
                        if item['material_type'] == 'Ткань':
                            result_text += f"{item['name']} ({material_name}): {item['quantity']} осталось\n"
                self.label_6.setText(result_text)
                self.label_6.adjustSize()

                # Обработка фурнитуры
                hardware_info = "Необходимая фурнитура:\n"
                for material_name, items in items_by_material.items():
                    for item in items:
                        if item['material_type'] == 'Фурнитура':
                            hardware_info += f"{item['name']} ({material_name}): {item['quantity']} шт\n"
                self.label_4.setText(hardware_info)
                self.label_4.adjustSize()

                # Проверка наличия материалов
                if all(item['quantity'] <= 0 for items in items_by_material.values()):
                    self.confirm_cutting(db)
                else:
                    self.show_material_request()

        except Exception as e:
            self.show_error_message(f"Ошибка расчета: {str(e)}")

    def confirm_cutting(self, db):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Question)
        msg.setText("Подтверждение раскроя")
        msg.setInformativeText("Все материалы доступны. Подтвердите раскрой.")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        if msg.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
            self.update_order_status(db, 'Ожидание материалов со склада')
            self.update_material_usage(db)

    def update_order_status(self, db, status):
        try:
            query = "UPDATE order_request SET status = %s WHERE id = %s"
            db.execute_query(query, (status, self.current_order['id']))
            self.show_order_page()
        except Exception as e:
            self.show_error_message(f"Ошибка обновления статуса заказа: {str(e)}")

    def update_material_usage(self, db):
        try:
            # Обновляем таблицу product_materials
            query = """
            UPDATE product_materials pm
            JOIN order_composition oc ON pm.order_composition_id = oc.id
            JOIN supply_composition sc ON pm.supply_composition_id = sc.id
            SET pm.quantity = GREATEST(pm.quantity - oc.quantity, 0),
                sc.remainder = GREATEST(sc.remainder - oc.quantity, 0)
            WHERE oc.order_id = %s AND sc.status = 'Доставлен'
            """
            db.execute_query(query, (self.current_order['id'],))

            # Добавляем данные в таблицу obrezki
            query = """
            INSERT INTO obrezki (material_id, length, width, remainder, creation_date, supply_composition_id)
            SELECT m.id, sc.length, sc.width, sc.remainder, CURDATE(), sc.id
            FROM supply_composition sc
            JOIN material m ON sc.material_id = m.id
            JOIN order_composition oc ON sc.id = oc.supply_composition_id
            WHERE oc.order_id = %s AND sc.remainder > 0
            """
            db.execute_query(query, (self.current_order['id'],))

        except Exception as e:
            self.show_error_message(f"Ошибка обновления использования материалов: {str(e)}")

    def show_material_request(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setText("Заявка на поставку материалов")
        msg.setInformativeText("Не хватает материалов. Оформите заявку на поставку.")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()
        self.update_order_status(self.db_manager, 'Заказ материалов')

    def pack_single_fabric(self, fabric_width, fabric_height, items):
        best_result = {'placements': [], 'used': [], 'area': 0}

        for rotation in [False, True]:
            temp_items = [item.copy() for item in items if item['quantity'] > 0]
            placements = []
            used = []
            free_space = [(0, 0, fabric_width, fabric_height)]

            for item in sorted(temp_items, key=lambda x: (-x['width'], -x['height'])):
                item_width = item['width'] if not rotation else item['height']
                item_height = item['height'] if not rotation else item['width']

                max_x = int(fabric_width // item_width)
                max_y = int(fabric_height // item_height)
                max_count = max_x * max_y
                possible_count = min(max_count, item['quantity'])

                if possible_count > 0:
                    placements.append({
                        'x': 0,
                        'y': 0,
                        'width': item_width,
                        'height': item_height,
                        'count': possible_count,
                        'name': item['name']
                    })
                    used.append({
                        'name': item['name'],
                        'count': possible_count
                    })
                    item['quantity'] -= possible_count

                    remaining_width = fabric_width - (max_x * item_width)
                    remaining_height = fabric_height - (max_y * item_height)

                    if remaining_width > 0:
                        free_space.append((
                            max_x * item_width,
                            0,
                            remaining_width,
                            fabric_height
                        ))

                    if remaining_height > 0:
                        free_space.append((
                            0,
                            max_y * item_height,
                            fabric_width,
                            remaining_height
                        ))

            total_area = sum(p['width'] * p['height'] * p['count'] for p in placements)
            if total_area > best_result['area']:
                best_result = {
                    'placements': placements,
                    'used': used,
                    'area': total_area
                }

        return best_result['placements'], best_result['used']

    def create_cutting_map(self, fabric_id, width, height, placements, material_name):
        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(600, 400)

        ax = fig.add_subplot(111)
        ax.set_title(f"{material_name} ({width}x{height} см)")
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.grid(True)

        ax.add_patch(plt.Rectangle(
            (0, 0), width, height,
            fill=False, edgecolor='black', lw=2
        ))

        for p in placements:
            for i in range(p['count']):
                row = i // int(width // p['width'])
                col = i % int(width // p['width'])

                x = col * p['width']
                y = row * p['height']

                rect = plt.Rectangle(
                    (x, y), p['width'], p['height'],
                    edgecolor='blue', facecolor='lightblue', alpha=0.5
                )
                ax.add_patch(rect)
                ax.text(
                    x + p['width'] / 2, y + p['height'] / 2,
                    f"{p['name']}\n{p['width']}x{p['height']}",
                    ha='center', va='center', fontsize=6
                )

        self.cutting_maps_container.add_cutting_map(canvas)

    def show_error_message(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText(text)
        msg.setWindowTitle("Ошибка")
        msg.exec()

    def show_order_page(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
