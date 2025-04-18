import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class Image:
    @staticmethod
    def new(mode, size, color):
        return None
    @staticmethod
    def open(filename):
        return None

class ImageTk:
    @staticmethod
    def PhotoImage(image):
        return None
class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Товары компании TechStore")
        self.root.minsize(800, 600)
        
        # Загрузка данных
        self.data_file = "products.json"
        self.products = []
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения
        self.update_display()
    
    def load_data(self):
        """Загрузка данных из JSON файла или создание тестовых данных"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.products = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
                self.create_sample_data()
        else:
            self.create_sample_data()
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def create_sample_data(self):
        """Создание тестовых данных"""
        self.products = [
            {
                "id": 1,
                "name": "Смартфон Galaxy S21",
                "description": "Флагманский смартфон с AMOLED экраном",
                "manufacturer": "Samsung",
                "price": 79990,
                "discount": 10,
                "image": None
            },
            {
                "id": 2,
                "name": "Ноутбук MacBook Pro",
                "description": "13 дюймов, процессор M1, 8 ГБ ОЗУ",
                "manufacturer": "Apple",
                "price": 129990,
                "discount": 15,
                "image": None
            },
            {
                "id": 3,
                "name": "Наушники WH-1000XM4",
                "description": "Беспроводные наушники с шумоподавлением",
                "manufacturer": "Sony",
                "price": 29990,
                "discount": 5,
                "image": None
            },
            {
                "id": 4,
                "name": "Планшет iPad Air",
                "description": "10.9 дюймов, процессор A14 Bionic",
                "manufacturer": "Apple",
                "price": 59990,
                "discount": 20,
                "image": None
            },
            {
                "id": 5,
                "name": "Умные часы Watch 3",
                "description": "Смарт-часы с функцией ECG",
                "manufacturer": "Huawei",
                "price": 19990,
                "discount": 0,
                "image": None
            }
        ]
        self.save_data()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Панель управления
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Фильтр по скидке
        ttk.Label(control_frame, text="Фильтр по скидке:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.discount_filter = ttk.Combobox(control_frame, values=[
            "Все диапазоны", 
            "0-9.99%", 
            "10-14.99%", 
            "15% и более"
        ], state="readonly")
        self.discount_filter.current(0)
        self.discount_filter.grid(row=0, column=1, padx=5)
        self.discount_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Сортировка
        ttk.Label(control_frame, text="Сортировка:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.sort_var = tk.StringVar(value="price_asc")
        ttk.Radiobutton(control_frame, text="Цена по возрастанию", variable=self.sort_var, 
                        value="price_asc", command=self.apply_filters).grid(row=0, column=3, padx=5)
        ttk.Radiobutton(control_frame, text="Цена по убыванию", variable=self.sort_var, 
                        value="price_desc", command=self.apply_filters).grid(row=0, column=4, padx=5)
        
        # Счетчик записей
        self.counter_label = ttk.Label(control_frame, text="")
        self.counter_label.grid(row=0, column=5, padx=5, sticky=tk.E)
        
        # Таблица с товарами
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Treeview с вертикальной прокруткой
        self.tree = ttk.Treeview(self.tree_frame, columns=("image", "name", "description", "manufacturer", "price", "discount"), 
                                show="headings", selectmode="browse")
        
        # Настройка столбцов
        self.tree.heading("image", text="Изображение")
        self.tree.heading("name", text="Наименование")
        self.tree.heading("description", text="Описание")
        self.tree.heading("manufacturer", text="Производитель")
        self.tree.heading("price", text="Цена")
        self.tree.heading("discount", text="Скидка")
        
        # Настройка ширины столбцов
        self.tree.column("image", width=100, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.W)
        self.tree.column("description", width=250, anchor=tk.W)
        self.tree.column("manufacturer", width=120, anchor=tk.W)
        self.tree.column("price", width=100, anchor=tk.E)
        self.tree.column("discount", width=80, anchor=tk.E)
        
        # Добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Привязываем событие изменения размера окна
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        pass
    
    def apply_filters(self, event=None):
        """Применение фильтров и сортировки"""
        self.update_display()
    
    def update_display(self):
        """Обновление отображения товаров с учетом фильтров и сортировки"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Применяем фильтр по скидке
        filtered_products = self.products.copy()
        discount_filter = self.discount_filter.get()
        
        if discount_filter == "0-9.99%":
            filtered_products = [p for p in filtered_products if 0 <= p["discount"] < 10]
        elif discount_filter == "10-14.99%":
            filtered_products = [p for p in filtered_products if 10 <= p["discount"] < 15]
        elif discount_filter == "15% и более":
            filtered_products = [p for p in filtered_products if p["discount"] >= 15]
        
        # Применяем сортировку
        sort_by = self.sort_var.get()
        if sort_by == "price_asc":
            filtered_products.sort(key=lambda x: x["price"])
        elif sort_by == "price_desc":
            filtered_products.sort(key=lambda x: x["price"], reverse=True)
        
        # Добавляем товары в таблицу
        for product in filtered_products:
            # Форматируем цену
            price_text = f"{product['price']} ₽"
            if product["discount"] > 0:
                final_price = product["price"] * (100 - product["discount"]) / 100
                price_text = f"~~{price_text}~~ {final_price:.0f} ₽"
            
            # Добавляем товар в таблицу
            item_id = self.tree.insert("", tk.END, values=(
                "",  # Изображение будет добавлено позже
                product["name"],
                product["description"],
                product["manufacturer"],
                price_text,
                f"{product['discount']}%"
            ))
            
            # Подсветка строки в зависимости от скидки
            if product["discount"] >= 15:
                self.tree.tag_configure("high_discount", background="#7fff00")
                self.tree.item(item_id, tags=("high_discount",))
            
            # Загрузка изображения (если есть)
            if product["image"] and os.path.exists(product["image"]):
                try:
                    img = Image.open(product["image"])
                    img.thumbnail((80, 80))
                    photo = ImageTk.PhotoImage(img)
                    self.tree.set(item_id, "image", "")
                    self.tree.image = photo  # Сохраняем ссылку на изображение
                    self.tree.item(item_id, image=photo)
                except Exception as e:
                    print(f"Ошибка загрузки изображения: {e}")
                    self.set_default_image(item_id)
            else:
                self.set_default_image(item_id)
        
        # Обновляем счетчик записей
        self.counter_label.config(text=f"{len(filtered_products)} из {len(self.products)}")
    
    def set_default_image(self, item_id):
        """Установка изображения-заглушки"""
        try:
            # Создаем черное изображение-заглушку
            img = Image.new("RGB", (80, 80), "lightgray")
            photo = ImageTk.PhotoImage(img)
            self.tree.set(item_id, "image", "")
            self.tree.image = photo  # Сохраняем ссылку на изображение
            self.tree.item(item_id, image=photo)
        except Exception as e:
            print(f"Ошибка создания изображения-заглушки: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()