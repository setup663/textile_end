-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Фев 19 2025 г., 00:55
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `product_up_2.0`
--

-- --------------------------------------------------------

--
-- Структура таблицы `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `login` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `organization_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `organization_type_id` int(11) DEFAULT NULL,
  `director_first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director_last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director_middle_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `kpp` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ogrn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `customer`
--

INSERT INTO `customer` (`id`, `login`, `password`, `organization_name`, `inn`, `organization_type_id`, `director_first_name`, `director_last_name`, `director_middle_name`, `kpp`, `ogrn`, `email`, `address`) VALUES
(1, 'home_textile', '12345', 'Домашний Текстиль', '7701234567', 1, 'Светлана', 'Иванова', 'Петровна', '770101001', '1027700532441', 'home@textile.ru', 'г. Москва, ул. Текстильная, д. 15, офис 34'),
(2, 'hotel_comfort', 'pass123', 'Отель Комфорт', '7701987654', 2, 'Андрей', 'Семенов', 'Викторович', '770501001', '1027700765432', 'hotel@comfort.com', 'г. Санкт-Петербург, Невский пр-т, д. 120'),
(6, 'style_lux', 'StYl3!2024', 'Стиль Люкс', '7703456789', 1, 'Ольга', 'Кузнецова', 'Сергеевна', '770301001', '1137700456321', 'info@style-lux.ru', 'г. Казань, ул. Пушкина, д. 45'),
(7, 'textile_house', 'Th2024pass', 'Текстиль Хаус', '7704567890', 4, 'Игорь', 'Николаев', 'Алексеевич', '770401002', '1147700234876', 'sales@textile-house.com', 'г. Екатеринбург, ул. Ленина, д. 72'),
(8, 'ip_vasiliev', 'vAs2024!', 'ИП Васильев П.И.', '7705678901', 3, 'Петр', 'Васильев', 'Иванович', NULL, '315774500123456', 'ip-vasiliev@mail.ru', 'г. Новосибирск, ул. Советская, д. 12');

-- --------------------------------------------------------

--
-- Структура таблицы `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `login` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `middle_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `passport_series` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passport_number` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci,
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `position_id` int(11) DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `employee`
--

INSERT INTO `employee` (`id`, `login`, `password`, `first_name`, `last_name`, `middle_name`, `birth_date`, `passport_series`, `passport_number`, `address`, `phone_number`, `position_id`, `email`) VALUES
(1, 'manager1', 'mgr1', 'Анна', 'Иванова', 'Сергеевна', '1990-05-25', '4505', '123456', 'г. Москва, ул. Тверская, д. 10, кв. 5', '+79167778899', 1, 'ivanova.ai@company.ru'),
(2, 'shveya1', 'shv1', 'Мария', 'Смирнова', 'Андреевна', '1988-08-14', '4511', '654321', 'г. Москва, ул. Парковая, д. 33, кв. 12', '+79035554433', 2, 'smirnova.ms@company.ru'),
(3, 'designer1', 'des1', 'Ольга', 'Кузнецова', 'Андреевна', '1990-02-20', '4515', '789012', 'г. Москва, ул. Дизайнерская, д. 8, кв. 15', '+79167778899', 5, NULL),
(6, 'ivanov.ai', 'Ivanov2024!', 'Алексей', 'Иванов', 'Игоревич', '1985-03-15', '4510', '123456', 'г. Москва, ул. Лермонтова, д. 7, кв. 34', '+79161234567', 2, 'ivanov.ai@company.ru'),
(7, 'petrova.mv', 'Petrova#2024', 'Мария', 'Петрова', 'Владимировна', '1992-07-22', '4512', '654321', 'г. Москва, ул. Гагарина, д. 12, кв. 89', '+79035671234', 3, 'petrova.mv@company.ru'),
(8, 'sidorov.da', 'SidorovDA24', 'Дмитрий', 'Сидоров', 'Анатольевич', '1988-11-05', '4508', '112233', 'г. Химки, ул. Центральная, д. 15', '+79168765432', 4, 'sidorov.da@company.ru'),
(9, 'kuznetsova.ep', 'KuznE2024', 'Елена', 'Кузнецова', 'Павловна', '1995-01-30', '4520', '334455', 'г. Москва, ул. Производственная, д. 5', '+79031237894', 5, 'kuznetsova.ep@company.ru'),
(10, 'smirnov.iv', 'Smirn0v!', 'Иван', 'Смирнов', 'Васильевич', '1979-12-12', '4501', '998877', 'г. Москва, пр-т Мира, д. 56, кв. 12', '+79150987654', 1, 'smirnov.iv@company.ru');

-- --------------------------------------------------------

--
-- Структура таблицы `furniture`
--

CREATE TABLE `furniture` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `furniture`
--

INSERT INTO `furniture` (`id`, `name`) VALUES
(1, 'Пуговицы'),
(2, 'Молнии'),
(3, 'Кнопки');

-- --------------------------------------------------------

--
-- Структура таблицы `location`
--

CREATE TABLE `location` (
  `id` int(11) NOT NULL,
  `row_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shelf_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `location`
--

INSERT INTO `location` (`id`, `row_number`, `shelf_number`) VALUES
(1, '1', '2'),
(2, '2', '2'),
(3, '3', '2'),
(4, '1', '3'),
(5, '2', '3');

-- --------------------------------------------------------

--
-- Структура таблицы `material`
--

CREATE TABLE `material` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `material_type_id` int(11) DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `material`
--

INSERT INTO `material` (`id`, `name`, `color`, `material_type_id`, `description`) VALUES
(1, 'Хлопок', 'Белый', 1, 'Натуральная ткань для постельного белья, 150 г/м²'),
(2, 'Сатин', 'Голубой', 1, 'Гладкая ткань для декора, 120 г/м²'),
(3, 'Пуговицы пластиковые', 'Белый', 2, 'Пластиковые пуговицы диаметром 15 мм'),
(4, 'Молния металлическая', 'Серебро', 2, 'Металлическая молния №5, длина 50 см');

-- --------------------------------------------------------

--
-- Структура таблицы `material_type`
--

CREATE TABLE `material_type` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_of_measure_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `material_type`
--

INSERT INTO `material_type` (`id`, `name`, `unit_of_measure_id`) VALUES
(1, 'Ткань', 2),
(2, 'Фурнитура', 1),
(3, 'Махровая ткань', 2),
(4, 'Тюль', 2);

-- --------------------------------------------------------

--
-- Структура таблицы `obrezki`
--

CREATE TABLE `obrezki` (
  `id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL,
  `length` decimal(10,2) NOT NULL,
  `width` decimal(10,2) NOT NULL,
  `remainder` decimal(10,2) NOT NULL,
  `creation_date` date NOT NULL,
  `supply_composition_id` int(11) NOT NULL,
  `is_used` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `obrezki`
--

INSERT INTO `obrezki` (`id`, `material_id`, `length`, `width`, `remainder`, `creation_date`, `supply_composition_id`, `is_used`) VALUES
(1, 1, '0.50', '1.50', '0.50', '2025-02-13', 1, 0),
(2, 2, '0.70', '2.00', '0.70', '2025-02-13', 2, 0),
(3, 1, '1.50', '0.00', '100.00', '2025-02-13', 1, 0),
(4, 2, '2.00', '0.00', '50.00', '2025-02-13', 2, 0),
(5, 3, '0.00', '0.00', '200.00', '2025-02-13', 3, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `okantovka`
--

CREATE TABLE `okantovka` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `okantovka`
--

INSERT INTO `okantovka` (`id`, `name`) VALUES
(1, 'Без окантовки'),
(2, 'Шёлковая'),
(3, 'Хлопковая');

-- --------------------------------------------------------

--
-- Структура таблицы `order_composition`
--

CREATE TABLE `order_composition` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `workshop_id` int(11) DEFAULT NULL,
  `total_sale_price` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `okantovka_id` int(11) DEFAULT NULL,
  `furniture_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `order_composition`
--

INSERT INTO `order_composition` (`id`, `order_id`, `product_id`, `quantity`, `width`, `length`, `workshop_id`, `total_sale_price`, `status`, `location_id`, `okantovka_id`, `furniture_id`) VALUES
(1, 1, 1, 10, '1.50', '2.00', 1, '5000.00', 'В производстве', NULL, 1, 1),
(2, 1, 2, 20, '0.70', '1.40', 2, '10000.00', 'В производстве', NULL, 2, NULL),
(3, 2, 3, 5, '1.50', '1.50', 1, '2500.00', 'В производстве', NULL, 3, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `order_request`
--

CREATE TABLE `order_request` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `status` enum('Новый','В обработке','В производстве','Выполнен','Отменен') COLLATE utf8mb4_unicode_ci DEFAULT 'Новый',
  `date` date DEFAULT NULL,
  `cost_price` decimal(10,2) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `order_request`
--

INSERT INTO `order_request` (`id`, `customer_id`, `employee_id`, `status`, `date`, `cost_price`, `total_price`) VALUES
(1, 1, 1, 'В обработке', '2025-02-13', '4500.00', '7500.00'),
(2, 2, 1, 'Новый', '2025-02-13', '9000.00', '12000.00');

-- --------------------------------------------------------

--
-- Структура таблицы `organization_type`
--

CREATE TABLE `organization_type` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `organization_type`
--

INSERT INTO `organization_type` (`id`, `name`) VALUES
(1, 'ООО'),
(2, 'ОАО'),
(3, 'ИП'),
(4, 'ЗАО'),
(5, 'НКО'),
(6, 'АО');

-- --------------------------------------------------------

--
-- Структура таблицы `position`
--

CREATE TABLE `position` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `position`
--

INSERT INTO `position` (`id`, `name`) VALUES
(1, 'Менеджер по закупкам'),
(2, 'Швея'),
(3, 'Кладовщик'),
(4, 'Мастер цеха'),
(5, 'Дизайнер'),
(6, 'Контролер качества');

-- --------------------------------------------------------

--
-- Структура таблицы `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `model` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_type_id` int(11) DEFAULT NULL,
  `unit_of_measure_id` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `product`
--

INSERT INTO `product` (`id`, `name`, `description`, `model`, `product_type_id`, `unit_of_measure_id`) VALUES
(1, 'Простынь двуспальная', 'Простынь из 100% хлопка, размер 220x240 см', 'PD-2024', 1, 1),
(2, 'Полотенце банное', 'Банное полотенце 70x140 см, плотность 500 г/м²', 'TB-2024', 2, 1),
(3, 'Скатерть 150x150', 'Квадратная скатерть с узором, 100% полиэстер', 'SK-2024', 3, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `product_materials`
--

CREATE TABLE `product_materials` (
  `id` int(11) NOT NULL,
  `order_composition_id` int(11) DEFAULT NULL,
  `supply_composition_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `cut_size` decimal(10,2) DEFAULT NULL,
  `cut_cost` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `product_materials`
--

INSERT INTO `product_materials` (`id`, `order_composition_id`, `supply_composition_id`, `quantity`, `cost`, `cut_size`, `cut_cost`) VALUES
(1, 1, 1, 15, NULL, '3.00', NULL),
(2, 2, 2, 10, NULL, '2.50', NULL),
(3, 3, 3, 8, NULL, '4.00', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `product_type`
--

CREATE TABLE `product_type` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `product_type`
--

INSERT INTO `product_type` (`id`, `name`) VALUES
(1, 'Постельное белье'),
(2, 'Полотенца'),
(3, 'Скатерти'),
(4, 'Шторы');

-- --------------------------------------------------------

--
-- Структура таблицы `supplier`
--

CREATE TABLE `supplier` (
  `id` int(11) NOT NULL,
  `organization_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `organization_type_id` int(11) DEFAULT NULL,
  `director_first_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director_last_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `director_middle_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `kpp` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ogrn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `supplier`
--

INSERT INTO `supplier` (`id`, `organization_name`, `inn`, `organization_type_id`, `director_first_name`, `director_last_name`, `director_middle_name`, `kpp`, `ogrn`, `email`, `address`) VALUES
(1, 'ТекстильПром', '7701123456', 1, 'Иван', 'Петров', 'Сергеевич', '770101001', '1027700123456', 'textile@mail.ru', 'г. Москва, ул. Текстильщиков, д. 10'),
(2, 'ФурнитураЛюкс', '7701987654', 1, 'Ольга', 'Сидорова', 'Игоревна', '770501001', '1027700654321', 'furnitura@yandex.ru', 'г. Подольск, ул. Заводская, д. 5'),
(3, 'ЭкоТекстиль', '7705123789', 4, 'Александр', 'Петров', 'Петрович', '770501002', '027700634123', 'eco-textile@gmail.com', 'г. Москва, ул. Новокузнецкая, д. 23, к3');

-- --------------------------------------------------------

--
-- Структура таблицы `supply`
--

CREATE TABLE `supply` (
  `id` int(11) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `supply`
--

INSERT INTO `supply` (`id`, `employee_id`, `supplier_id`, `total_amount`, `date`) VALUES
(1, 1, 1, '15000.00', '2024-02-01'),
(2, 1, 2, '5000.00', '2024-02-05');

-- --------------------------------------------------------

--
-- Структура таблицы `supply_composition`
--

CREATE TABLE `supply_composition` (
  `id` int(11) NOT NULL,
  `supply_id` int(11) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `unit_quantity` int(11) DEFAULT NULL,
  `unit_count` int(11) DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `remainder` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `supply_composition`
--

INSERT INTO `supply_composition` (`id`, `supply_id`, `material_id`, `quantity`, `length`, `width`, `cost`, `unit_quantity`, `unit_count`, `status`, `location_id`, `remainder`) VALUES
(1, 1, 1, 100, '1.50', '0.00', '120.00', 1, 100, 'Доставлено', 1, 100),
(2, 1, 2, 50, '2.00', '0.00', '180.00', 1, 50, 'Доставлено', 2, 50),
(3, 2, 3, 200, '0.00', '0.00', '15.00', 1, 200, 'Доставлено', 3, 200);

--
-- Триггеры `supply_composition`
--
DELIMITER $$
CREATE TRIGGER `after_supply_composition_update` AFTER UPDATE ON `supply_composition` FOR EACH ROW BEGIN
    DECLARE v_unit_id INT;
    
    -- Создаем обрезки только если остаток > 0.3
    IF NEW.remainder > 0.3 THEN
        -- Добавляем запись в obrezki
        INSERT INTO obrezki (
            material_id, 
            length, 
            width, 
            remainder, 
            creation_date, 
            supply_composition_id
        ) VALUES (
            NEW.material_id,
            NEW.length,
            NEW.width,
            NEW.remainder,
            CURDATE(),
            NEW.id
        );
        
        -- Получаем unit_id из типа материала
        SELECT mt.unit_of_measure_id 
        INTO v_unit_id
        FROM material m
        JOIN material_type mt 
            ON m.material_type_id = mt.id
        WHERE m.id = NEW.material_id;
        
        -- Добавляем обрезки на склад
        INSERT INTO warehouse (
            storage_type_id,
            obrezki_id,
            amount,
            unit_id,
            entry_date
        ) VALUES (
            3,  -- storage_type_id = 3 (Обрезки)
            LAST_INSERT_ID(),  -- ID новой записи в obrezki
            NEW.remainder,
            v_unit_id,
            CURDATE()
        );
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `unit_of_measure`
--

CREATE TABLE `unit_of_measure` (
  `id` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `symbol` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `unit_of_measure`
--

INSERT INTO `unit_of_measure` (`id`, `name`, `symbol`) VALUES
(1, 'Штука', 'шт'),
(2, 'Метр', 'м'),
(3, 'Сантиметр', 'см'),
(4, 'Квадратный метр', 'м²'),
(5, 'Упаковка', 'упк');

-- --------------------------------------------------------

--
-- Структура таблицы `warehouse_movement`
--

CREATE TABLE `warehouse_movement` (
  `id` int(11) NOT NULL,
  `supply_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `movement_type` enum('Приход','Расход') COLLATE utf8mb4_unicode_ci NOT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `creation_date` date NOT NULL,
  `supply_cost` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `warehouse_movement`
--

INSERT INTO `warehouse_movement` (`id`, `supply_id`, `location_id`, `movement_type`, `width`, `length`, `creation_date`, `supply_cost`) VALUES
(1, 1, 4, 'Приход', '0.00', '150.00', '2024-02-01', '15000.00'),
(2, 2, 2, 'Приход', '0.00', '110.00', '2024-02-05', '5000.00');

-- --------------------------------------------------------

--
-- Структура таблицы `workshop`
--

CREATE TABLE `workshop` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `workshop`
--

INSERT INTO `workshop` (`id`, `name`) VALUES
(1, 'Цех раскроя'),
(2, 'Цех пошива'),
(3, 'Цех упаковки');

-- --------------------------------------------------------

--
-- Структура таблицы `workshop_employee`
--

CREATE TABLE `workshop_employee` (
  `id` int(11) NOT NULL,
  `workshop_id` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `workshop_employee`
--

INSERT INTO `workshop_employee` (`id`, `workshop_id`, `employee_id`) VALUES
(1, 1, 2),
(2, 2, 3),
(3, 1, 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_customer_organization_type` (`organization_type_id`);

--
-- Индексы таблицы `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `position_id` (`position_id`);

--
-- Индексы таблицы `furniture`
--
ALTER TABLE `furniture`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_material_material_type` (`material_type_id`);

--
-- Индексы таблицы `material_type`
--
ALTER TABLE `material_type`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_material_type_unit` (`unit_of_measure_id`);

--
-- Индексы таблицы `obrezki`
--
ALTER TABLE `obrezki`
  ADD PRIMARY KEY (`id`),
  ADD KEY `material_id` (`material_id`),
  ADD KEY `supply_composition_id` (`supply_composition_id`);

--
-- Индексы таблицы `okantovka`
--
ALTER TABLE `okantovka`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `order_composition`
--
ALTER TABLE `order_composition`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_order_composition_order` (`order_id`),
  ADD KEY `fk_order_composition_product` (`product_id`),
  ADD KEY `fk_order_composition_workshop` (`workshop_id`),
  ADD KEY `fk_order_composition_location` (`location_id`),
  ADD KEY `fk_order_okantovka` (`okantovka_id`),
  ADD KEY `fk_order_furniture` (`furniture_id`);

--
-- Индексы таблицы `order_request`
--
ALTER TABLE `order_request`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_order_request_customer` (`customer_id`),
  ADD KEY `fk_order_request_employee` (`employee_id`);

--
-- Индексы таблицы `organization_type`
--
ALTER TABLE `organization_type`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `position`
--
ALTER TABLE `position`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_product_product_type` (`product_type_id`),
  ADD KEY `fk_product_unit_of_measure` (`unit_of_measure_id`);

--
-- Индексы таблицы `product_materials`
--
ALTER TABLE `product_materials`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_product_materials_order_composition` (`order_composition_id`),
  ADD KEY `fk_product_materials_supply_composition` (`supply_composition_id`);

--
-- Индексы таблицы `product_type`
--
ALTER TABLE `product_type`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_supplier_organization_type` (`organization_type_id`);

--
-- Индексы таблицы `supply`
--
ALTER TABLE `supply`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_supply_employee` (`employee_id`),
  ADD KEY `fk_supply_supplier` (`supplier_id`);

--
-- Индексы таблицы `supply_composition`
--
ALTER TABLE `supply_composition`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_supply_composition_supply` (`supply_id`),
  ADD KEY `fk_supply_composition_material` (`material_id`),
  ADD KEY `fk_supply_composition_location` (`location_id`);

--
-- Индексы таблицы `unit_of_measure`
--
ALTER TABLE `unit_of_measure`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `warehouse_movement`
--
ALTER TABLE `warehouse_movement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supply_id` (`supply_id`),
  ADD KEY `location_id` (`location_id`);

--
-- Индексы таблицы `workshop`
--
ALTER TABLE `workshop`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `workshop_employee`
--
ALTER TABLE `workshop_employee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_workshop_employee_workshop` (`workshop_id`),
  ADD KEY `fk_workshop_employee_employee` (`employee_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `furniture`
--
ALTER TABLE `furniture`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `location`
--
ALTER TABLE `location`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `material`
--
ALTER TABLE `material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `material_type`
--
ALTER TABLE `material_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `obrezki`
--
ALTER TABLE `obrezki`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `okantovka`
--
ALTER TABLE `okantovka`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `order_composition`
--
ALTER TABLE `order_composition`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `order_request`
--
ALTER TABLE `order_request`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `organization_type`
--
ALTER TABLE `organization_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `position`
--
ALTER TABLE `position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `product_materials`
--
ALTER TABLE `product_materials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `product_type`
--
ALTER TABLE `product_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `supplier`
--
ALTER TABLE `supplier`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `supply`
--
ALTER TABLE `supply`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `supply_composition`
--
ALTER TABLE `supply_composition`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `unit_of_measure`
--
ALTER TABLE `unit_of_measure`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `warehouse_movement`
--
ALTER TABLE `warehouse_movement`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `workshop`
--
ALTER TABLE `workshop`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `workshop_employee`
--
ALTER TABLE `workshop_employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `fk_customer_organization_type` FOREIGN KEY (`organization_type_id`) REFERENCES `organization_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_employee_position` FOREIGN KEY (`position_id`) REFERENCES `position` (`id`);

--
-- Ограничения внешнего ключа таблицы `material`
--
ALTER TABLE `material`
  ADD CONSTRAINT `fk_material_material_type` FOREIGN KEY (`material_type_id`) REFERENCES `material_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `material_type`
--
ALTER TABLE `material_type`
  ADD CONSTRAINT `fk_material_type_unit` FOREIGN KEY (`unit_of_measure_id`) REFERENCES `unit_of_measure` (`id`);

--
-- Ограничения внешнего ключа таблицы `obrezki`
--
ALTER TABLE `obrezki`
  ADD CONSTRAINT `obrezki_ibfk_1` FOREIGN KEY (`material_id`) REFERENCES `material` (`id`),
  ADD CONSTRAINT `obrezki_ibfk_2` FOREIGN KEY (`supply_composition_id`) REFERENCES `supply_composition` (`id`);

--
-- Ограничения внешнего ключа таблицы `order_composition`
--
ALTER TABLE `order_composition`
  ADD CONSTRAINT `fk_order_composition_order` FOREIGN KEY (`order_id`) REFERENCES `order_request` (`id`),
  ADD CONSTRAINT `fk_order_composition_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `fk_order_composition_workshop` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`),
  ADD CONSTRAINT `fk_order_furniture` FOREIGN KEY (`furniture_id`) REFERENCES `furniture` (`id`),
  ADD CONSTRAINT `fk_order_okantovka` FOREIGN KEY (`okantovka_id`) REFERENCES `okantovka` (`id`);

--
-- Ограничения внешнего ключа таблицы `order_request`
--
ALTER TABLE `order_request`
  ADD CONSTRAINT `fk_order_request_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  ADD CONSTRAINT `fk_order_request_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`);

--
-- Ограничения внешнего ключа таблицы `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `fk_product_product_type` FOREIGN KEY (`product_type_id`) REFERENCES `product_type` (`id`),
  ADD CONSTRAINT `fk_product_unit_of_measure` FOREIGN KEY (`unit_of_measure_id`) REFERENCES `unit_of_measure` (`id`);

--
-- Ограничения внешнего ключа таблицы `product_materials`
--
ALTER TABLE `product_materials`
  ADD CONSTRAINT `fk_product_materials_order_composition` FOREIGN KEY (`order_composition_id`) REFERENCES `order_composition` (`id`),
  ADD CONSTRAINT `fk_product_materials_supply_composition` FOREIGN KEY (`supply_composition_id`) REFERENCES `supply_composition` (`id`);

--
-- Ограничения внешнего ключа таблицы `supplier`
--
ALTER TABLE `supplier`
  ADD CONSTRAINT `fk_supplier_organization_type` FOREIGN KEY (`organization_type_id`) REFERENCES `organization_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `supply`
--
ALTER TABLE `supply`
  ADD CONSTRAINT `fk_supply_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  ADD CONSTRAINT `fk_supply_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`id`);

--
-- Ограничения внешнего ключа таблицы `supply_composition`
--
ALTER TABLE `supply_composition`
  ADD CONSTRAINT `fk_supply_composition_material` FOREIGN KEY (`material_id`) REFERENCES `material` (`id`),
  ADD CONSTRAINT `fk_supply_composition_supply` FOREIGN KEY (`supply_id`) REFERENCES `supply` (`id`),
  ADD CONSTRAINT `supply_composition_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `warehouse_movement`
--
ALTER TABLE `warehouse_movement`
  ADD CONSTRAINT `warehouse_movement_ibfk_1` FOREIGN KEY (`supply_id`) REFERENCES `supply` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `warehouse_movement_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE SET NULL;

--
-- Ограничения внешнего ключа таблицы `workshop_employee`
--
ALTER TABLE `workshop_employee`
  ADD CONSTRAINT `fk_workshop_employee_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  ADD CONSTRAINT `fk_workshop_employee_workshop` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
