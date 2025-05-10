-- Вставка категорий
INSERT INTO firstproject_category (name, description) VALUES
('Натуральный мёд', 'Различные сорта натурального мёда'),
('Продукты пчеловодства', 'Сопутствующие продукты пчеловодства');

-- Вставка тегов
INSERT INTO firstproject_tag (name, description) VALUES
('Свежий', 'Свежий урожай'),
('Органический', 'Экологически чистый продукт'),
('Подарочная упаковка', 'Товар в подарочной упаковке'),
('Акция', 'Товар участвует в акции');

-- Вставка товаров
INSERT INTO firstproject_product (
    name, 
    description, 
    price, 
    image, 
    created_at, 
    updated_at, 
    is_deleted, 
    category_id
) VALUES
('Липовый мёд', 'Ароматный мёд из липовых цветов', 1500.00, NULL, NOW(), NOW(), false, 1),
('Гречишный мёд', 'Тёмный мёд с гречишных полей', 1200.00, NULL, NOW(), NOW(), false, 1),
('Цветочный мёд', 'Смесь разнотравья', 1000.00, NULL, NOW(), NOW(), false, 1),
('Акациевый мёд', 'Нежный и светлый мёд', 1700.00, NULL, NOW(), NOW(), false, 1),
('Прополис', 'Натуральный прополис', 500.00, NULL, NOW(), NOW(), false, 2),
('Пчелиный воск', 'Чистый пчелиный воск', 300.00, NULL, NOW(), NOW(), false, 2);

-- Связи товаров с тегами (many-to-many)
INSERT INTO firstproject_product_tags (product_id, tag_id) VALUES
(1, 1), (1, 2),
(2, 1),
(3, 2), (3, 4),
(4, 3),
(5, 2), (5, 4),
(6, 3);

-- Вставка заказов
INSERT INTO firstproject_order (
    number, 
    created_at, 
    delivery_address, 
    phone, 
    full_name
) VALUES
('ORD001', NOW(), 'ул. Пчелкина, 1', '+79123456789', 'Иванов Иван Иванович'),
('ORD002', NOW(), 'пр. Медовый, 5', '+79234567890', 'Петрова Мария Сергеевна'),
('ORD003', NOW(), 'ул. Цветочная, 10', '+79345678901', 'Сидоров Алексей Викторович');

-- Вставка позиций заказов
INSERT INTO firstproject_orderitem (
    order_id, 
    product_id, 
    quantity, 
    discount
) VALUES
(1, 1, 2, 100.00),
(1, 5, 1, 0.00),
(1, 3, 3, 50.00),
(2, 2, 1, 0.00),
(2, 4, 2, 150.00),
(2, 6, 4, 0.00),
(3, 5, 2, 100.00),
(3, 1, 1, 0.00);

UPDATE firstproject_product 
SET image = 'products/acacia_medium.jpg' 
WHERE name = 'Акациевый мёд';

UPDATE firstproject_product 
SET image = 'products/cvetochniy_medium.jpg' 
WHERE name = 'Цветочный мёд';

UPDATE firstproject_product 
SET image = 'products/grechishniy_medium.jpg' 
WHERE name = 'Гречишный мёд';

UPDATE firstproject_product 
SET image = 'products/lipoviy_medium.jpg' 
WHERE name = 'Липовый мёд';

UPDATE firstproject_product 
SET image = 'products/propolis.jpg' 
WHERE name = 'Прополис';

UPDATE firstproject_product 
SET image = 'products/vosk.jpg' 
WHERE name = 'Пчелиный воск';

select * from firstproject_product
