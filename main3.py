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
                      self.label_rascr, self.label_5, self.label_7]:
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
                SELECT pm.supply_composition_id, pm.quantity, sc.width, sc.length, m.name as material_name
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
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
                            'material_name': fabric['material_name']
                    }
                    else:
                        fabrics[fabric_id]['quantity'] += int(fabric['quantity'])

                # Отображаем доступные материалы
                fabric_info = "\n".join([
                    f"{data['material_name']} #{fabric_id}: {data['width']}x{data['height']} см, {data['quantity']} шт"
                    for fabric_id, data in fabrics.items()
                ])
                self.label_3.setText(f"Доступные полотна ткани:\n{fabric_info}")
                self.label_3.adjustSize()

                # Получаем изделия в заказе
                order_query = """
                SELECT oc.id, p.name, oc.quantity, oc.width, oc.length
                FROM order_composition oc
                JOIN product p ON oc.product_id = p.id
                WHERE oc.order_id = %s
                """
                order_items = db.execute_query(order_query, (order['id'],))

                total_products = sum(item['quantity'] for item in order_items)
                self.label_2.setText(f"Требуется изделий: {total_products}")
                self.label_2.adjustSize()

                total_area = sum(item['width'] * item['length'] * item['quantity']
                             for item in order_items)
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
                SELECT pm.supply_composition_id, pm.quantity, sc.width, sc.length, m.name as material_name
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
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
                            'material_name': fabric['material_name']
                    }
                    else:
                        fabrics[fabric_id]['quantity'] += int(fabric['quantity'])

                # Получаем изделия в заказе
                order_query = """
                SELECT oc.id, p.name, oc.quantity, oc.width, oc.length, m.name as material_name
                FROM order_composition oc
                JOIN product p ON oc.product_id = p.id
                JOIN product_materials pm ON oc.id = pm.order_composition_id
                JOIN material m ON pm.supply_composition_id = m.id
                WHERE oc.order_id = %s
                """
                order_items = db.execute_query(order_query, (self.current_order['id'],))

                # Группируем изделия по материалам
                items_by_material = {}
                for item in order_items:
                    material_name = item['material_name']
                    if material_name not in items_by_material:
                        items_by_material[material_name] = []
                    items_by_material[material_name].append({
                        'name': item['name'],
                        'width': float(item['width']),
                        'height': float(item['length']),
                        'quantity': int(item['quantity'])
                    })

                # Проверяем наличие материалов
                all_materials_available = True
                for material_name, items in items_by_material.items():
                    required_area = sum(item['width'] * item['height'] * item['quantity'] for item in items)
                    available_area = sum(fabric['width'] * fabric['height'] * fabric['quantity']
                                         for fabric in fabrics.values() if fabric['material_name'] == material_name)
                    if required_area > available_area:
                        all_materials_available = False
                        break

                if all_materials_available:
                    # Если все материалы доступны
                    reply = QtWidgets.QMessageBox.question(
                        self, 'Подтверждение', 'Все материалы доступны. Подтвердить раскрой?',
                        QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
                    )
                    if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                        # Обновляем статус заказа
                        update_query = """
                        UPDATE order_request SET status = 'Ожидание материалов со склада' WHERE id = %s
                        """
                        db.execute_query(update_query, (self.current_order['id'],))

                        # Обновляем таблицу supply_composition
                        for fabric_id, fabric in fabrics.items():
                            update_supply_query = """
                            UPDATE supply_composition SET status = 'Доставлен', location_id = NULL WHERE id = %s
                            """
                            db.execute_query(update_supply_query, (fabric_id,))

                        # Обновляем таблицу product_materials
                        for material_name, items in items_by_material.items():
                            for item in items:
                                insert_product_materials_query = """
                                INSERT INTO product_materials (order_composition_id, supply_composition_id, quantity)
                                VALUES (%s, %s, %s)
                                """
                                db.execute_query(insert_product_materials_query, (item['id'], fabric_id, item['quantity']))

                        # Обновляем таблицу obrezki
                        for fabric_id, fabric in fabrics.items():
                            insert_obrezki_query = """
                            INSERT INTO obrezki (material_id, length, width, remainder, creation_date, supply_composition_id)
                            VALUES (%s, %s, %s, %s, CURDATE(), %s)
                            """
                            db.execute_query(insert_obrezki_query, (fabric['material_id'], fabric['width'], fabric['height'], 0, fabric_id))

                        self.show_order_page()
                    else:
                        return
                else:
                    # Если материалов не хватает
                    self.show_error_message('Не хватает материалов. Оформите заявку на поставку материалов.')
                    # update_query = """
                    # UPDATE order_request SET status = 'Заказ материалов' WHERE id = %s
                    # """
                    # db.execute_query(update_query, (self.current_order['id'],))

                    # Создаем заявку на поставку новых материалов
                    for material_name, items in items_by_material.items():
                        required_area = sum(item['width'] * item['height'] * item['quantity'] for item in items)
                        available_area = sum(fabric['width'] * fabric['height'] * fabric['quantity']
                                             for fabric in fabrics.values() if fabric['material_name'] == material_name)
                        if required_area > available_area:
                            # Вычисляем недостающее количество материала
                            missing_quantity = required_area // (fabric['width'] * fabric['length'])

                            insert_supply_composition_query = """
                            INSERT INTO supply_composition (supply_id, material_id, quantity, width, length, status)
                            VALUES (%s, %s, %s, %s, %s, 'Новый')
                            """
                            db.execute_query(insert_supply_composition_query, (None, fabric['material_id'], missing_quantity, fabric['width'], fabric['length']))

        except Exception as e:
            self.show_error_message(f"Ошибка расчета: {str(e)}")
            print(f"Ошибка расчета: {str(e)}")

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
