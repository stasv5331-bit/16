"""
Основная логика для задания 2
"""
import logging
import math
from typing import List, Tuple, Dict, Any
from array_operations import validate_arrays, safe_power, ArrayValidationError

logger = logging.getLogger(__name__)

class CalculationError(Exception):
    """Исключение для ошибок вычислений"""
    pass

class PowerCalculationError(CalculationError):
    """Исключение для ошибок при возведении в степень"""
    pass

def process_task2(arr1: List[int], arr2: List[int], arr3: List[int]) -> List[float]:
    """
    Основная функция для задания 2
    
    Алгоритм:
    1. Проверяем, могут ли два числа под одним и тем же номером в сумме давать третье число
    2. Если могут, то сумма трех чисел возводится в степень наименьшего числа
    
    Args:
        arr1: Первый массив чисел
        arr2: Второй массив чисел
        arr3: Третий массив чисел
        
    Returns:
        List[float]: Результаты вычислений для каждого индекса
        
    Raises:
        ArrayValidationError: Если массивы невалидны
        CalculationError: Если произошла ошибка вычислений
    """
    logger.info("Начало обработки задания 2")
    
    try:
        # Валидация входных данных
        validate_arrays(arr1, arr2, arr3)
        
        results = []
        
        for i in range(len(arr1)):
            try:
                a, b, c = arr1[i], arr2[i], arr3[i]
                
                # Проверка условия a + b == c
                if a + b == c:
                    logger.debug(f"Элемент {i}: условие выполнено ({a} + {b} = {c})")
                    
                    # Сумма трех чисел
                    total_sum = a + b + c
                    
                    # Наименьшее число из трех
                    min_value = min(a, b, c)
                    
                    try:
                        # Возведение в степень
                        if min_value < 0:
                            logger.warning(f"Отрицательная степень: {min_value}")
                        
                        result = safe_power(total_sum, min_value)
                        results.append(float(result))
                        
                        logger.info(f"Элемент {i}: ({a}+{b}+{c})^{min_value} = {result}")
                        
                    except ValueError as e:
                        logger.error(f"Ошибка при возведении в степень для элемента {i}: {e}")
                        results.append(float('nan'))  # Not a Number для ошибок
                        
                else:
                    logger.debug(f"Элемент {i}: условие не выполнено ({a} + {b} != {c})")
                    results.append(0.0)
                    
            except Exception as e:
                logger.error(f"Ошибка при обработке элемента {i}: {e}")
                results.append(float('nan'))
        
        logger.info(f"Обработка завершена. Получено {len(results)} результатов")
        return results
        
    except ArrayValidationError as e:
        logger.error(f"Ошибка валидации массивов: {e}")
        raise
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при обработке: {e}")
        raise CalculationError(f"Ошибка вычислений: {e}") from e

def calculate_statistics(results: List[float]) -> Dict[str, Any]:
    """
    Расчет статистики по результатам
    
    Args:
        results: Список результатов вычислений
        
    Returns:
        Dict: Статистика результатов
    """
    logger.info("Расчет статистики результатов")
    
    try:
        # Фильтруем валидные результаты (не NaN и не бесконечность)
        valid_results = []
        for r in results:
            if isinstance(r, (int, float)) and not math.isnan(r) and not math.isinf(r):
                valid_results.append(r)
        
        if not valid_results:
            logger.warning("Нет валидных результатов для статистики")
            return {
                'total_count': len(results),
                'valid_count': 0,
                'successful_count': len([r for r in results if r != 0]),
                'mean': 0,
                'min': 0,
                'max': 0,
                'has_errors': any(math.isnan(r) or math.isinf(r) for r in results)
            }
        
        stats = {
            'total_count': len(results),
            'valid_count': len(valid_results),
            'successful_count': len([r for r in results if r != 0]),
            'mean': sum(valid_results) / len(valid_results),
            'min': min(valid_results),
            'max': max(valid_results),
            'has_errors': any(math.isnan(r) or math.isinf(r) for r in results)
        }
        
        logger.debug(f"Статистика: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Ошибка при расчете статистики: {e}")
        return {'error': str(e)}

def generate_test_data(size: int = 5, min_val: int = 1, max_val: int = 10) -> Tuple[List[int], List[int], List[int]]:
    """
    Генерация тестовых данных
    
    Args:
        size: Размер массивов
        min_val: Минимальное значение
        max_val: Максимальное значение
        
    Returns:
        tuple: Три массива тестовых данных
    """
    import random
    
    logger.info(f"Генерация тестовых данных: size={size}, range=[{min_val}, {max_val}]")
    
    try:
        if size <= 0:
            raise ValueError("Размер должен быть положительным")
        if min_val > max_val:
            raise ValueError("Минимальное значение должно быть меньше максимального")
        
        arr1 = [random.randint(min_val, max_val) for _ in range(size)]
        arr2 = [random.randint(min_val, max_val) for _ in range(size)]
        
        # Генерируем arr3 так, чтобы примерно в половине случаев условие выполнялось
        arr3 = []
        for i in range(size):
            if random.random() > 0.5:
                # Условие выполняется
                arr3.append(arr1[i] + arr2[i])
            else:
                # Условие не выполняется
                arr3.append(random.randint(min_val * 2, max_val * 2))
        
        return arr1, arr2, arr3
        
    except Exception as e:
        logger.error(f"Ошибка генерации тестовых данных: {e}")
        raise

def demonstrate_workflow():
    """Демонстрация рабочего процесса"""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОЧЕГО ПРОЦЕССА")
    print("=" * 60)
    
    test_cases = [
        {
            'name': 'Корректные данные с выполнением условий',
            'arr1': [1, 2, 3],
            'arr2': [4, 5, 6],
            'arr3': [5, 7, 9]  # 1+4=5, 2+5=7, 3+6=9
        },
        {
            'name': 'Частичное выполнение условий',
            'arr1': [1, 2, 3],
            'arr2': [2, 3, 4],
            'arr3': [3, 6, 7]  # 1+2=3, 2+3≠6, 3+4=7
        },
        {
            'name': 'Сгенерированные данные',
            'data': 'generate'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*40}")
        print(f"ТЕСТ {i}: {test['name']}")
        print('='*40)
        
        try:
            if test.get('data') == 'generate':
                arr1, arr2, arr3 = generate_test_data(3)
            else:
                arr1, arr2, arr3 = test['arr1'], test['arr2'], test['arr3']
            
            print(f"Массив 1: {arr1}")
            print(f"Массив 2: {arr2}")
            print(f"Массив 3: {arr3}")
            
            results = process_task2(arr1, arr2, arr3)
            stats = calculate_statistics(results)
            
            print(f"\nРезультаты: {results}")
            print(f"\nСтатистика:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
        except ArrayValidationError as e:
            print(f"✗ Ошибка валидации: {e}")
        except CalculationError as e:
            print(f"✗ Ошибка вычислений: {e}")
        except Exception as e:
            print(f"✗ Неожиданная ошибка: {type(e).__name__}: {e}")