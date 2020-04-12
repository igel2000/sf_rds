import numpy as np
import collections

def game_core_v2(number, left_border, right_border):
    '''Поиск загаданного чилас бинарным поиском (делением пополам)
       Параметры:
         - number  - загаданное число
         - left_border, right_border - границы, в которых загадано число.
       Возвращает количество сделанных ходов
    '''
    #счетчик попыток
    count = 1  
    #первая попытка предсказания - середина диапазона
    predict = (right_border - left_border) // 2  
    while number != predict:
        #пока не угадали, значит будет еще одна попытка
        count+=1
        if number > predict:   # загаданное число больше предсказания
            #вычислим смещение для будущего прогноза
            a = (right_border - predict) // 2  
            #сдвинем левую границу на предыдущий прогноз,
            #и сделаем новый прогноз. Если посчитанное смещение 
            #было равно 0, то увеличим прогноз на 1
            left_border, predict = predict, predict + (a if a else 1)  
        else: 
            #вычислим смещение для будущего прогноза
            a = (predict - left_border) // 2
            #сдвинем правую границу на предыдущий прогноз,
            #и сделаем новый прогноз. Если посчитанное смещение 
            #было равно 0, то уменьшим прогноз на 1
            right_border, predict = predict, predict - (a if a else 1)
    return(count) 

def score_game(game_core, left_border, right_border, size, random_seed):
    ''' Прогнать одну сессию игры
    В ходе сессии игра запускается size раз с разными загаданными числами.
    По итогам запусков считается и выводится среднее число ходов, за которое угадывались числа
    Параметры:
      - game_core: функция, которая собственно ищет число
      - left_border, right_border - границы, в которых загадывается число
      - size: сколько раз прогнать игру
      - random_seed - параметр для инициализации генератора случайных чисел для загадывания чисел
    '''
    count_ls = []
    np.random.seed(random_seed)
    random_array = np.random.randint(left_border, right_border+1, size=(size))
    c = collections.Counter()
    for number in random_array:
        t = game_core(number, left_border, right_border)
        count_ls.append(t)
        c[t] += 1
    score = np.mean(count_ls)
    print(f"Алгоритм угадывает число от {left_border} до {right_border} в среднем за {score} попыток.")
    print(f"random_seed = {random_seed}, статистика по количеству попыток: {c}")
    return(score)