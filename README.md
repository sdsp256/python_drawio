# История изменений

| Версия  | Дата       | Описание изменений                                     |
|---------|------------|--------------------------------------------------------|
| 0.09.01 | 2025-03-21 | MVP. Добавлен каталог для хранение диаграмм на github. |
| 0.09.00 | 2023-03-20 | Версия для Jupyter notebook                            |


### Configure project

#### 01. install modules 
```
pip install ipython
pip install re
```

#### 02. git clone code from github
```
git clone https://github.com/sdsp256/python_drawio
git branch -M main
git remote add origin https://github.com/sdsp256/python_drawio.git
git remote set-url origin git@github.com:sdsp256/python_drawio.git
```

#### 02.1 send changes to github 
```git push -u origin main```

#### 02.2 get changes for git
```
git pull
```

#### 3. run drawio gnerator 
```
python main.py
```

#### 4. create or modify diagram 
./diagrams - directory with diagram description and result draw.io 

#### 5. push after diagram created or modified 
```
git commit -m -a "2025-03-21 new diagram_name created"
```

#### 6. add row in table on top of document with notice 

| 0.09.00 | 2023-03-22 | add new flow diagram_name                            |



