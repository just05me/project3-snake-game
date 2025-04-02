import tkinter as tk
import random

# Настройки игры
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SNAKE_SIZE = 20
GAME_SPEED = 150

class SnakeGame:
    def __init__(self, root):
        # Сохраняем окно
        self.my_window = root

        # Имя окна
        self.my_window.title("Змейка")
        
        # Делаем окно для рисования
        self.my_canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        
        # Показываем окно
        self.my_canvas.pack()
        
        # Счёт игры
        self.my_score = 0
        
        # Показываем счёт
        self.score_text = tk.Label(root, text="Счёт: 0", font=("Arial", 14), fg="white", bg="black")
        self.score_text.place(x=WINDOW_WIDTH - 80, y=10)
        
        # Кнопка для старта
        self.start_button = tk.Button(root, text="Start", command=self.start_game, font=("Arial", 14))
        self.start_button.pack()
        
        # Кусочки змейки
        self.snake_body = []
        
        # Куда ползёт
        self.snake_direction = "right"
        
        # Где еда
        self.food_position = None
        
        # Идёт ли игра
        self.game_running = False

    # Функция для начала игры
    def start_game(self):
        # Убираем кнопку Старт
        self.start_button.pack_forget()

        # Делаем змейку из одного кусочка
        self.snake_body = [{"x": 300, "y": 300}]
        
        # Ползём вправо
        self.snake_direction = "right"
        
        # Ставим еду
        self.food_position = self.make_food()
        self.my_score = 0
        self.update_my_score()

        self.game_running = True
        
        # Кнопки на клавиатуре
        self.my_window.bind("<Key>", self.change_my_direction)
        self.play_game()

    # Функция для создания еды
    def make_food(self):
        food_x = random.randint(0, (WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        new_food = {"x": food_x, "y": food_y}

        return new_food

    # Функция для движения змейки
    def move_my_snake(self):
        # Копируем голову
        head_x = self.snake_body[0]["x"]
        head_y = self.snake_body[0]["y"]

        # Двигаем в зависимости от направления
        if self.snake_direction == "up":
            head_y = head_y - SNAKE_SIZE  # вверх
        elif self.snake_direction == "down":
            head_y = head_y + SNAKE_SIZE  # вниз
        elif self.snake_direction == "left":
            head_x = head_x - SNAKE_SIZE  # влево
        elif self.snake_direction == "right":
            head_x = head_x + SNAKE_SIZE  # вправо
        
        # Телепортация
        if head_x >= WINDOW_WIDTH:
            head_x = 0
        elif head_x < 0:
            head_x = WINDOW_WIDTH - SNAKE_SIZE
        if head_y >= WINDOW_HEIGHT:
            head_y = 0
        elif head_y < 0:
            head_y = WINDOW_HEIGHT - SNAKE_SIZE
        
        # Добавляем новую голову - вставляем в начало
        new_head = {"x": head_x, "y": head_y}
        self.snake_body.insert(0, new_head)
        
        # Проверяем - еда съедена?
        if head_x == self.food_position["x"] and head_y == self.food_position["y"]:
            self.food_position = self.make_food()
            
            # Плюс 1 счёт - обновляем счёт
            self.my_score = self.my_score + 1
            self.update_my_score()
        else:
            # Удаляем хвост
            self.snake_body.pop()  

    # Функция для обновления счёта
    def update_my_score(self):
        # Меняет текст
        self.score_text.config(text="Счёт: " + str(self.my_score))

    # Функция для столкновения
    def check_if_hit(self):
        # Смотрим - где голова?
        head_x = self.snake_body[0]["x"]
        head_y = self.snake_body[0]["y"]

        # Проверяем все кусочки - кроме головы
        for i in range(1, len(self.snake_body)):
            part_x = self.snake_body[i]["x"]
            part_y = self.snake_body[i]["y"]
            
            if head_x == part_x and head_y == part_y:
                return True  
        
        return False

    # Функция для смены направления
    def change_my_direction(self, event):
        # Какая кнопка нажалась
        key = event.keysym

        if key == "Up" and self.snake_direction != "down":
            self.snake_direction = "up"
        elif key == "Down" and self.snake_direction != "up":
            self.snake_direction = "down"
        elif key == "Left" and self.snake_direction != "right":
            self.snake_direction = "left"
        elif key == "Right" and self.snake_direction != "left":
            self.snake_direction = "right"

    # Функция для рисования
    def draw_my_game(self):
        # Чистим окно
        self.my_canvas.delete("all")

        # Рисуем змейку
        for part in self.snake_body:
            x1 = part["x"]
            y1 = part["y"]
            x2 = x1 + SNAKE_SIZE
            y2 = y1 + SNAKE_SIZE
            self.my_canvas.create_rectangle(x1, y1, x2, y2, fill="green")

        # Рисуем еду
        food_x1 = self.food_position["x"]
        food_y1 = self.food_position["y"]
        food_x2 = food_x1 + SNAKE_SIZE
        food_y2 = food_y1 + SNAKE_SIZE
        self.my_canvas.create_rectangle(food_x1, food_y1, food_x2, food_y2, fill="red")

    # Функция для игры
    def play_game(self):
        if self.game_running == True:
            self.move_my_snake()

            # Проверяем - врезались?
            if self.check_if_hit() == True:  
                
                # Game over
                self.game_running = False  
                
                # Пишем, что игра окончена
                self.my_canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Игра окончена!", font=("Arial", 20), fill="white")
                
                # Показываем кнопку Старт
                self.start_button.pack()  
            else:
                self.draw_my_game()  
                
                # Ждём и повторяем
                self.my_window.after(GAME_SPEED, self.play_game)

# Запускаем игру
my_window = tk.Tk()
game = SnakeGame(my_window)
my_window.mainloop()