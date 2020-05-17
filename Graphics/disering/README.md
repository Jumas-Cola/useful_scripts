# Алгоритм рассеивания ошибок Флойда-Стейнберга

```python
fs_dithering('img.jpg')
```
Рассеивание ошибок происходит по следующей схеме:

              X   7/16
    3/16   5/16   1/16  

  
![fs_dithering](img_fs_disered.bmp)
 
 # Псевдотонирование с упорядоченным размытием
 
 ```python
ordered_dithering('img.jpg', size=4)
```
Изображение разбивается на зоны, равные по размеру матрице порогов. К каждой зоне применяется данная матрица. Если текущий пиксель составляет меньше, чем 255 * <порог>, то он приравнивается 0 иначе 255.

Матрица имеет следующий вид (предварительно к каждому элементу матрицы прибавляется 1):  
![baer_matr](https://wikimedia.org/api/rest_v1/media/math/render/svg/e70fec3d485fcb6e7f6eff901632169aad4ba649)

В результате получается матрица порогов такого вида:  
![limit_matr](https://wikimedia.org/api/rest_v1/media/math/render/svg/160becbdbca71c9253f76118cbf8defb4572d754)

Матрицы с измерениями, равными степеням двойки, могут быть вычислены по рекурсивной формуле:  
![ordered_dithering](https://wikimedia.org/api/rest_v1/media/math/render/svg/1a5107bdaaf9b9415cf998929196b016a5dc2b14)

  
![ordered_dithering](img_ordered_disered.bmp)

Источник:
https://habr.com/ru/post/326936/
