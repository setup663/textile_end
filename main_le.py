import sys
import logging
import configparser
from PyQt6 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pymysql
from texti import Ui_Form  # Ваш модуль с описанием интерфейса

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

    def execute_insert(self, query, params=None):
        """Выполняет INSERT-запрос и возвращает lastrowid."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Insert error: {str(e)}")
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

        # Словари для хранения недостающих материалов
        self.fabric_shortage = {}    # для ткани (material_type != 'Фурнитура')
        self.hardware_shortage = {}  # для фурнитуры (определяется через material_type.name = 'Фурнитура')
        self.shortage_data = {}      # объединённые данные

        # Инициализируем область для отображения карт раскроя (для ткани)
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
                      self.label_5, self.label_rascr, self.label_7]:
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
                # Загрузка данных по полотнам ткани для заказа (исключая фурнитуру)
                fabric_query = """
                SELECT pm.supply_composition_id, pm.quantity, sc.width, sc.length, m.name as material_name
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
                INNER JOIN order_composition oc ON pm.order_composition_id = oc.id
                WHERE oc.order_id = %s AND m.material_type_id != 2
                """
                fabric_data = db.execute_query(fabric_query, (order['id'],))
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

                fabric_info = "\n".join([
                    f"{data['material_name']} #{fabric_id}: {data['width']}x{data['height']} см, {data['quantity']} шт"
                    for fabric_id, data in fabrics.items()
                ])
                self.label_3.setText(f"Доступные полотна ткани:\n{fabric_info}")
                self.label_3.adjustSize()

                # Загрузка данных по изделиям заказа (для подсчёта общего количества изделий и площади)
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

                total_area = sum(item['width'] * item['length'] * item['quantity'] for item in order_items)
                self.label_5.setText(f"Общая площадь ткани: {total_area} см²")
                self.label_5.adjustSize()

                # Загрузка информации по фурнитуре (через material_type.name = 'Фурнитура')
                required_query = """
                SELECT m.name as hardware_name, SUM(pm.quantity) as required
                FROM product_materials pm
                JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                JOIN material m ON sc.material_id = m.id
                JOIN material_type mt ON m.material_type_id = mt.id
                WHERE pm.order_composition_id IN (SELECT id FROM order_composition WHERE order_id = %s)
                  AND mt.name = 'Фурнитура'
                GROUP BY m.name
                """
                required_data = db.execute_query(required_query, (order['id'],))
                available_query = """
                SELECT m.name as hardware_name, SUM(sc.quantity) as available
                FROM supply_composition sc
                JOIN material m ON sc.material_id = m.id
                JOIN material_type mt ON m.material_type_id = mt.id
                WHERE mt.name = 'Фурнитура'
                GROUP BY m.name
                """
                available_data = db.execute_query(available_query)
                hardware_info_lines = []
                self.hardware_shortage = {}
                for req in required_data:
                    hardware_name = req['hardware_name']
                    required_qty = req['required']
                    available_qty = 0
                    for avail in available_data:
                        if avail['hardware_name'] == hardware_name:
                            available_qty = avail['available']
                            break
                    hardware_info_lines.append(
                        f"{hardware_name}: требуется {required_qty} шт, доступно {available_qty} шт"
                    )
                    if required_qty > available_qty:
                        self.hardware_shortage[hardware_name] = required_qty - available_qty

                self.label_4.setText("Фурнитура:\n" + "\n".join(hardware_info_lines))
                self.label_4.adjustSize()
                # Здесь больше не вызываем check_and_prompt_supply_request,
                # чтобы дополнительные окна не появлялись при выборе заказа.
        except Exception as e:
            self.show_error_message(f"Ошибка загрузки данных: {str(e)}")

    def calculate_cutting(self):
        """
        При нажатии на pushButton_calculate_rascr происходит расчёт необходимых полотен ткани,
        а также проверка наличия материалов. Дополнительные окна (информационные и предупреждения)
        будут показаны только в этом методе.
        """
        if not self.current_order:
            return

        try:
            self.cutting_maps_container.clear_maps()

            with self.db_manager as db:
                # Получаем данные по полотнам ткани для изделий заказа (исключая фурнитуру)
                fabric_query = """
                SELECT pm.supply_composition_id, sc.width, sc.length, m.name as material_name
                FROM product_materials pm
                INNER JOIN supply_composition sc ON pm.supply_composition_id = sc.id
                INNER JOIN material m ON sc.material_id = m.id
                INNER JOIN order_composition oc ON pm.order_composition_id = oc.id
                WHERE oc.order_id = %s AND m.material_type_id != 2
                """
                fabric_data = db.execute_query(fabric_query, (self.current_order['id'],))
                # Группируем по материалу – используем первую запись для каждого материала
                fabrics_by_material = {}
                for fabric in fabric_data:
                    mat_name = fabric['material_name']
                    if mat_name not in fabrics_by_material:
                        fabrics_by_material[mat_name] = {
                            'supply_composition_id': fabric['supply_composition_id'],
                            'width': float(fabric['width']),
                            'height': float(fabric['length']),
                            'material_name': mat_name
                        }

                # Получаем изделия заказа для материалов (ткани)
                order_query = """
                SELECT oc.id, p.name, oc.quantity, oc.width, oc.length, m.name as material_name
                FROM order_composition oc
                JOIN product p ON oc.product_id = p.id
                JOIN product_materials pm ON oc.id = pm.order_composition_id
                JOIN material m ON pm.supply_composition_id = m.id
                WHERE oc.order_id = %s AND m.material_type_id != 2
                """
                order_items = db.execute_query(order_query, (self.current_order['id'],))
                # Группируем изделия по материалу
                items_by_material = {}
                for item in order_items:
                    mat_name = item['material_name']
                    if mat_name not in items_by_material:
                        items_by_material[mat_name] = []
                    items_by_material[mat_name].append({
                        'name': item['name'],
                        'width': float(item['width']),
                        'height': float(item['length']),
                        'quantity': int(item['quantity'])
                    })

                total_fabric_required = {}
                # Для каждого материала рассчитываем число полотен, необходимых для выполнения заказа
                for material, items in items_by_material.items():
                    if material not in fabrics_by_material:
                        continue
                    fabric_info = fabrics_by_material[material]
                    fabric_width = fabric_info['width']
                    fabric_height = fabric_info['height']
                    supply_composition_id = fabric_info['supply_composition_id']

                    items_copy = [item.copy() for item in items]
                    fabric_required = 0
                    while any(item['quantity'] > 0 for item in items_copy):
                        valid_items = [item for item in items_copy if item['quantity'] > 0]
                        placements, used = self.pack_single_fabric(fabric_width, fabric_height, valid_items)
                        if placements:
                            self.create_cutting_map(supply_composition_id, fabric_width, fabric_height, placements, material)
                            for u in used:
                                for item in items_copy:
                                    if item['name'] == u['name']:
                                        item['quantity'] -= u['count']
                                        break
                            fabric_required += 1
                        else:
                            break
                    total_fabric_required[material] = fabric_required

                # Получаем общее количество ткани на складе
                available_fabric_query = """
                SELECT m.name as material_name, SUM(sc.quantity) as available
                FROM supply_composition sc
                JOIN material m ON sc.material_id = m.id
                WHERE m.material_type_id != 2
                GROUP BY m.name
                """
                available_fabric = db.execute_query(available_fabric_query)
                available_dict = {row['material_name']: row['available'] for row in available_fabric}

                self.fabric_shortage = {}
                for material, required in total_fabric_required.items():
                    available = available_dict.get(material, 0)
                    if required > available:
                        self.fabric_shortage[material] = required - available

                result_text = "Необходимо полотен ткани для выполнения заказа:\n"
                for material, count in total_fabric_required.items():
                    result_text += f"{material}: {count} шт\n"
                self.label_6.setText(result_text)
                self.label_6.adjustSize()

                # Теперь вызываем проверку наличия материалов и обновление статуса
                self.check_and_prompt_supply_request()

        except Exception as e:
            self.show_error_message(f"Ошибка расчёта: {str(e)}")

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
                        free_space.append((max_x * item_width, 0, remaining_width, fabric_height))
                    if remaining_height > 0:
                        free_space.append((0, max_y * item_height, fabric_width, remaining_height))

            total_area = sum(p['width'] * p['height'] * p['count'] for p in placements)
            if total_area > best_result['area']:
                best_result = {
                    'placements': placements,
                    'used': used,
                    'area': total_area
                }

        return best_result['placements'], best_result['used']

    def create_cutting_map(self, fabric_id, width, height, placements, material_name):
        # Фурнитура не отображается в картах раскроя – здесь только ткань
        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(600, 400)

        ax = fig.add_subplot(111)
        ax.set_title(f"{material_name} ({width}x{height} см)")
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.grid(True)

        ax.add_patch(plt.Rectangle((0, 0), width, height, fill=False, edgecolor='black', lw=2))
        for p in placements:
            for i in range(p['count']):
                row = i // int(width // p['width'])
                col = i % int(width // p['width'])
                x = col * p['width']
                y = row * p['height']
                rect = plt.Rectangle((x, y), p['width'], p['height'],
                                     edgecolor='blue', facecolor='lightblue', alpha=0.5)
                ax.add_patch(rect)
                ax.text(x + p['width'] / 2, y + p['height'] / 2,
                        f"{p['name']}\n{p['width']}x{p['height']}",
                        ha='center', va='center', fontsize=6)
        self.cutting_maps_container.add_cutting_map(canvas)

    def check_and_prompt_supply_request(self):
        """
        Проверяет наличие недостающих материалов и обновляет статус заказа:
         - Если по всем материалам (ткани и фурнитуры) недостача отсутствует, то статус меняется на "Готово в цеху".
         - Если для недостающих материалов доступен достаточный остаток (remainder) в поставках,
           то нужное количество автоматически переводится из remainder в product_materials, и статус меняется на "Раскрой".
         - Иначе, пользователю предлагается создать заявку на поставку, после чего статус обновится на "Заказ материалов".
        """
        self.shortage_data = {}
        for material, shortage in self.fabric_shortage.items():
            if shortage > 0:
                self.shortage_data[material] = shortage
        for material, shortage in self.hardware_shortage.items():
            if shortage > 0:
                self.shortage_data[material] = shortage

        with self.db_manager as db:
            # Проверяем, хватает ли материалов для выполнения заказа
            check_query = """
            SELECT m.name as material_name, SUM(pm.quantity) as required, COALESCE(SUM(sc.quantity), 0) as available
            FROM product_materials pm
            JOIN supply_composition sc ON pm.supply_composition_id = sc.id
            JOIN material m ON sc.material_id = m.id
            JOIN order_composition oc ON pm.order_composition_id = oc.id
            WHERE oc.order_id = %s
            GROUP BY m.name
            """
            material_check = db.execute_query(check_query, (self.current_order['id'],))

            all_materials_available = True
            for row in material_check:
                material_name = row['material_name']
                required = row['required']
                available = row['available']
                if required > available:
                    all_materials_available = False
                    self.shortage_data[material_name] = required - available

            if all_materials_available:
                # Все материалы имеются в product_materials – меняем статус на "Готово в цеху"
                db.execute_query("UPDATE order_request SET status = %s WHERE id = %s", ("Готово в цеху", self.current_order['id']))
                info_box = QtWidgets.QMessageBox(self)
                info_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                info_box.setWindowTitle("Заказ готов")
                info_box.setText("Все материалы есть. Статус заказа изменен на 'Готово в цеху'.")
                info_box.setStyleSheet("QLabel { color: white; } QPushButton { color: white; }")
                info_box.exec()
            else:
                # Если каких-то материалов не хватает, но они есть в остатках (remainder)
                all_available = True
                for material, shortage in self.shortage_data.items():
                    result = db.execute_query(
                        "SELECT SUM(remainder) as total_remainder FROM supply_composition sc JOIN material m ON sc.material_id = m.id WHERE m.name = %s",
                        (material,)
                    )
                    total_remainder = result[0]['total_remainder'] if result and result[0]['total_remainder'] is not None else 0
                    if total_remainder < shortage:
                        all_available = False
                        break
                if all_available:
                    for material, shortage in self.shortage_data.items():
                        needed = shortage
                        rows = db.execute_query(
                            "SELECT sc.id, sc.remainder FROM supply_composition sc JOIN material m ON sc.material_id = m.id WHERE m.name = %s AND sc.remainder > 0 ORDER BY sc.id",
                            (material,)
                        )
                        for row in rows:
                            if needed <= 0:
                                break
                            available = row['remainder']
                            transfer_amount = min(available, needed)
                            oc_res = db.execute_query(
                                "SELECT oc.id FROM order_composition oc JOIN product_materials pm ON oc.id = pm.order_composition_id JOIN material m ON pm.supply_composition_id = m.id WHERE oc.order_id = %s AND m.name = %s LIMIT 1",
                                (self.current_order['id'], material)
                            )
                            if not oc_res:
                                oc_res = db.execute_query(
                                    "SELECT id FROM order_composition WHERE order_id = %s LIMIT 1",
                                    (self.current_order['id'],)
                                )
                            if oc_res:
                                oc_id = oc_res[0]['id']
                                db.execute_insert(
                                    "INSERT INTO product_materials (order_composition_id, supply_composition_id, quantity, cost, cut_size, cut_cost) VALUES (%s, %s, %s, NULL, NULL, NULL)",
                                    (oc_id, row['id'], transfer_amount)
                                )
                            db.execute_query("UPDATE supply_composition SET remainder = remainder - %s WHERE id = %s", (transfer_amount, row['id']))
                            needed -= transfer_amount
                    db.execute_query("UPDATE order_request SET status = %s WHERE id = %s", ("Раскрой", self.current_order['id']))
                    info_box = QtWidgets.QMessageBox(self)
                    info_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    info_box.setWindowTitle("Материалы переведены")
                    info_box.setText("Материалы из остатка поставок переведены в заказ. Статус заказа изменен на 'Раскрой'.")
                    info_box.setStyleSheet("QLabel { color: white; } QPushButton { color: white; }")
                    info_box.exec()
                else:
                    details = "\n".join([f"{k}: не хватает {v} шт" for k, v in self.shortage_data.items()])
                    msg_box = QtWidgets.QMessageBox(self)
                    msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    msg_box.setWindowTitle("Недостаточно материалов")
                    msg_box.setText("Для выполнения заказа не хватает следующих материалов:\n" + details)
                    msg_box.setStyleSheet("QLabel { color: white; } QPushButton { color: white; }")
                    create_btn = msg_box.addButton("Создать заявку", QtWidgets.QMessageBox.ButtonRole.AcceptRole)
                    cancel_btn = msg_box.addButton("Отмена", QtWidgets.QMessageBox.ButtonRole.RejectRole)
                    msg_box.exec()
                    if msg_box.clickedButton() == create_btn:
                        self.create_supply_requests()

    def create_supply_requests(self):
        """
        Для каждого материала, у которого обнаружена недостача, создаём:
         - запись в таблице supply,
         - запись в supply_composition (status 'новый', remainder = 0),
         - запись в product_materials (связь с order_composition).
         Затем обновляем статус заказа на 'Заказ материалов'.
        """
        try:
            with self.db_manager as db:
                for material_name, shortage in self.shortage_data.items():
                    mat_res = db.execute_query("SELECT id FROM material WHERE name = %s", (material_name,))
                    if not mat_res:
                        continue
                    material_id = mat_res[0]['id']
                    supply_id = db.execute_insert(
                        "INSERT INTO supply (employee_id, supplier_id, total_amount, date) VALUES (%s, %s, %s, CURDATE())",
                        (1, None, 0)
                    )
                    sc_id = db.execute_insert(
                        "INSERT INTO supply_composition (supply_id, material_id, quantity, length, width, cost, unit_quantity, unit_count, status, location_id, remainder) VALUES (%s, %s, %s, NULL, NULL, NULL, NULL, NULL, %s, NULL, %s)",
                        (supply_id, material_id, shortage, "новый", 0)
                    )
                    oc_res = db.execute_query(
                        "SELECT oc.id FROM order_composition oc "
                        "JOIN product_materials pm ON oc.id = pm.order_composition_id "
                        "JOIN material m ON pm.supply_composition_id = m.id "
                        "WHERE oc.order_id = %s AND m.name = %s LIMIT 1",
                        (self.current_order['id'], material_name)
                    )
                    if oc_res:
                        oc_id = oc_res[0]['id']
                        db.execute_insert(
                            "INSERT INTO product_materials (order_composition_id, supply_composition_id, quantity, cost, cut_size, cut_cost) VALUES (%s, %s, %s, NULL, NULL, NULL)",
                            (oc_id, sc_id, shortage)
                        )
                db.execute_query("UPDATE order_request SET status = %s WHERE id = %s", ("Заказ материалов", self.current_order['id']))
            info_box = QtWidgets.QMessageBox(self)
            info_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            info_box.setWindowTitle("Заявка создана")
            info_box.setText("Заявка на материалы успешно создана.")
            info_box.setStyleSheet("QLabel { color: white; } QPushButton { color: white; }")
            info_box.exec()
        except Exception as e:
            self.show_error_message(f"Ошибка создания заявки: {str(e)}")

    def show_error_message(self, text):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText(text)
        msg.setWindowTitle("Ошибка")
        msg.setStyleSheet("QLabel { color: white; } QPushButton { color: white; }")
        msg.exec()

    def show_order_page(self):
        self.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
