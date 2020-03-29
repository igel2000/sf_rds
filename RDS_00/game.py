import numpy as np
import collections

def game_core_v2(number, leftBorder, rightBorder):
    '''Ищем загаданное число бинарным поиском (делением пополам)
       number  - загаданное число
       leftBorder, rightBorder - границы, в которых загадано число.
       Функция возвращает число попыток
    '''
    #счетчик попыток
    count = 1  
    #первая попытка предсказания - середина диапазона
    predict = (rightBorder - leftBorder) // 2  
    while number != predict:
        #пока не угадали, значит будет еще одна попытка
        count+=1
        if number > predict:   # загаданное число больше предсказания
            #вычислим смещение для будущего прогноза
            a = (rightBorder - predict) // 2  
            #сдвинем левую границу на предыдущий прогноз,
            #и сделаем новый прогноз. Если посчитанное смещение 
            #было равно 0, то увеличим прогноз на 1
            leftBorder, predict = predict, predict + (a if a else 1)  
        else: 
            #вычислим смещение для будущего прогноза
            a = (predict - leftBorder) // 2
            #сдвинем правую границу на предыдущий прогноз,
            #и сделаем новый прогноз. Если посчитанное смещение 
            #было равно 0, то уменьшим прогноз на 1
            rightBorder, predict = predict, predict - (a if a else 1)
    return(count) 

def score_game(game_core_v1, leftBorder, rightBorder, size, random_seed):
    '''Запускаем игру size раз, чтоб узнать как быстро игра угадывает число
    leftBorder, rightBorder - границы, в которых загадывается число
    '''
    count_ls = []
    np.random.seed(random_seed)  # фиксируем RANDOM SEED = 1, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(leftBorder, rightBorder+1, size=(size))
    c = collections.Counter()
    for number in random_array:
        t = game_core_v1(number, leftBorder, rightBorder)
        count_ls.append(t)
        c[t] += 1
    score = np.mean(count_ls)
    print(f"Алгоритм угадывает число от {leftBorder} до {rightBorder} в среднем за {score} попыток.")
    print(f"random_seed = {random_seed}, статистика по количеству попыток: {c}")
    return(score)

# Проверяем
tc = 100
s = 0
for i in range(tc):
    s += score_game(game_core_v2, 1, 100, 1000, 1)
print(s / tc)    
