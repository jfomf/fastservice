from pathlib import Path
from PIL import Image
import re

root = Path(__file__).resolve().parent
old = (root / 'main.tex').read_text(encoding='utf-8')
preamble = old.split('\\begin{document}', 1)[0]
preamble = re.sub(r'\\input\{finance_assumptions\.tex\}.*?(?=\\definecolor)', '', preamble, flags=re.S)
preamble = preamble.replace(r'\fontsize{11}{14}\selectfont', r'\fontsize{10}{12.5}\selectfont')

def frame(n, label, title, items, image=None, note=None):
    out = [r'\begin{frame}[plain]', rf'\slidebegin{{{label}}}{{{title}}}{{{n}}}']
    if image:
        if image.startswith('../assets/'):
            iw, ih = Image.open(root / image).size
            size = 'width=62mm' if iw / ih < 62 / 48 else 'height=48mm'
            out += [r'\begin{scope}', r'\clip (88,16) rectangle (150,64);',
                    rf'\node[anchor=center,inner sep=0] at (119,40) {{\includegraphics[{size}]{{{image}}}}};',
                    r'\end{scope}']
        else:
            out.append(rf'\node[anchor=center,inner sep=0] at (119,40) {{\includegraphics[width=61mm,height=48mm,keepaspectratio]{{{image}}}}};')
        x, width = 10, 70
    else:
        x, width = 10, 138
    positions = [61, 44, 27] if len(items) == 3 else [59, 33]
    for y, (heading, body) in zip(positions, items):
        out.append(rf'\labeltext{{{x}}}{{{y}}}{{{width}}}{{{heading}}}')
        out.append(rf'\bodytext{{{x}}}{{{y-8}}}{{{width}}}{{{body}}}')
    out += [r'\slideend', r'\end{frame}']
    return '\n'.join(out)

slides = []
slides.append(r'''\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay,x=1mm,y=1mm]
\begin{scope}[shift={(current page.south west)}]
\fill[Paper] (0,0) rectangle (160,90);
\node[anchor=west,text=Coral,font=\bfseries\fontsize{12}{14}\selectfont] at (10,84) {Ладно · Ярославль};
\node[anchor=north west,text width=75mm,align=left,text=Ink,font=\bfseries\fontsize{24}{28}\selectfont] at (10,65) {Ремонт дома\\без поиска мастера};
\node[anchor=north west,text width=70mm,align=left,text=Ink,font=\fontsize{12}{16}\selectfont] at (10,38) {Одна заявка. Смета до выезда. Мы сами организуем мастера и проверим работу.};
\node[anchor=west,text=Muted,font=\fontsize{10}{12}\selectfont] at (10,13) {План пилота · демо-день 2026};
\node[anchor=center,inner sep=0] at (119,44) {\includegraphics[width=62mm,height=59mm,keepaspectratio]{../assets/stock/pipe-repair.jpg}};
\end{scope}\end{tikzpicture}\end{frame}''')
slides.append(frame(2,'Проблема','В воскресенье течёт сифон. Мастера ещё нет',[
    ('Что делает клиент','Открывает площадку, сравнивает профили и пишет нескольким людям.'),
    ('Что остаётся неизвестным','Кто сможет приехать сегодня, сколько будет стоить ремонт и кто отвечает за результат.')],
    '../assets/stock/tap.jpg','Сценарий бытовой поломки · фото: Pexels'))
slides.append(frame(3,'Сейчас','Клиент сам ведёт весь процесс',[
    ('Поиск и согласование','Выбирает площадку, пишет мастерам, ждёт цену и время приезда.'),
    ('Приёмка','Сам проверяет работу и решает спорные вопросы.')],
    '../assets/stock/fuse-box.jpg','Типовой путь клиента, а не измеренное время поиска'))
slides.append(frame(4,'Решение','Клиенту достаточно одной заявки',[
    ('Клиент','Описывает поломку, прикладывает фото и оставляет телефон.'),
    ('Ладно','Готовит смету, назначает мастера и ведёт заказ до результата.')],
    'site-home-crop.png','Скриншот действующего frontend-прототипа; звонки пока не подключены'))
slides.append(frame(5,'После заявки','Не ждать ответа неделями — стандарт пилота',[
    ('Первые минуты','Оператор должен перезвонить в течение 5 минут.'),
    ('До выезда','Главный мастер готовит смету. Диспетчер назначает исполнителя.')],
    '../assets/stock/worker3.jpg','5 минут — целевой стандарт пилота, не достигнутый показатель'))
slides.append(frame(6,'Цена','Смета видна до приезда мастера',[
    ('В примере заказа','Выезд и диагностика — 900 ₽, работа — 1 600 ₽, материалы — 350 ₽.'),
    ('Итого','2 850 ₽ до выезда. Другую работу согласуют отдельно.')],
    'site-quote-crop.png','Суммы — демонстрационный пример в прототипе'))
slides.append(frame(7,'Диспетчерская','Поиск и замена мастера — наша работа',[
    ('Назначение','Диспетчер видит фото, адрес, срочность и смету в одном заказе.'),
    ('Отказ исполнителя','Система предлагает следующего подходящего мастера; клиент не начинает поиск заново.')],
    'site-dispatcher-crop.png','Функция переназначения работает в демо'))
slides.append(frame(8,'Исполнители','Мастера работают по одному стандарту',[
    ('До допуска','Проверяем навыки и обучаем работе по чек-листу.'),
    ('На заказе','Заранее знает задачу. После ремонта показывает результат и убирает мусор.')],
    '../assets/stock/socket-work.jpg','Стандарт для запуска пилота; фото: Pexels'))
slides.append(frame(9,'Качество','Приёмка не заканчивается словом «готово»',[
    ('Чек-лист','Проверка результата вместе с клиентом, фото до и после, уборка места работы.'),
    ('Ответственность','Условия гарантии и итоговая сумма фиксируются в заказе.')],
    '../assets/stock/clean-tools.jpg','Чек-лист — планируемый операционный стандарт'))
slides.append(frame(10,'Прозрачность','Клиент видит, кто едет и что уже сделано',[
    ('Карточка мастера','Фото, специализация, предыдущие работы и отзывы.'),
    ('Заказ','Смета, этапы и фотоотчёт. Пока это показано на демо-данных.')],
    '../assets/stock/clean-faucet.jpg','В прототипе профили и отзывы демонстрационные'))
slides.append(frame(11,'Категории','На старте — сантехника и электрика',[
    ('Сантехника','Течь под раковиной, смеситель, сифон, засор.'),
    ('Электрика','Розетка, свет, диагностика щита.')],
    '../assets/stock/electrician.jpg','Две категории для пилота в Ярославле'))
slides.append(frame(12,'Скорость','Срочные заявки — отдельный маршрут',[
    ('Цель','Выезд в течение часа при наличии свободного мастера.'),
    ('Выходные и праздники','Нужны дежурства и резерв. Если окно занято, сразу назовём доступное время.')],
    '../assets/stock/valves.jpg','Время выезда и дежурства проверим на реальных заказах'))
slides.append(frame(13,'Ярославль','Пилот запускаем по районам, а не «везде»',[
    ('Первый контур','Кировский, Ленинский и Фрунзенский районы: проверяем маршруты и доступность мастеров.'),
    ('Затем','Расширение на Дзержинский и Красноперекопский районы после замера времени выезда.')],
    '../assets/stock/yaroslavl.jpg','Районы — план пилота; фото действительно снято в Ярославле'))
slides.append(frame(14,'Первые заявки','Конкретные каналы для старта',[
    ('Яндекс Директ','Поисковые объявления по запросам «сантехник срочно Ярославль», «электрик на дом Ярославль».'),
    ('Карты','Карточки сервиса в Яндекс Картах и 2ГИС: услуги, часы работы, зона выезда, телефон.'),
    ('Локально','Объявления Авито по двум категориям и рекомендации после выполненных заказов.')],
    None,'Это план размещения, не действующие кампании'))
slides.append(frame(15,'Роли','Кто отвечает за каждый шаг',[
    ('Оператор и диспетчер','Принимают заявку, назначают мастера и следят за временем.'),
    ('Главный мастер','Проверяет смету, обучает исполнителей и контролирует сложные случаи.')],
    '../assets/stock/electric-panel.jpg','Состав команды для пилота формируется; фото: Pexels'))
slides.append(frame(16,'Оплата','Клиенту не нужно рассчитываться с каждым',[
    ('Единый заказ','Сумма и состав работ видны до выезда. После ремонта — одна оплата.'),
    ('Сейчас','В прототипе оплата условная; реальный платёжный сервис ещё подключить.')],
    'site-estimate.png','Оплата — часть продуктового плана, не работающая платёжная система'))
slides.append(frame(17,'Пилот','Проверим обещания на реальных заказах',[
    ('Скорость','Время от заявки до ответа и от заявки до приезда по каждому району.'),
    ('Цена','Сколько смет меняется после осмотра и почему.'),
    ('Качество','Повторные обращения, выполнение чек-листа и отзывы клиентов.')],
    None,'Данных о продажах и выполненных заказах пока нет'))
slides.append(r'''\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay,x=1mm,y=1mm]
\begin{scope}[shift={(current page.south west)}]
\fill[Paper] (0,0) rectangle (160,90);
\node[anchor=west,text=Coral,font=\bfseries\fontsize{12}{14}\selectfont] at (10,84) {Следующий шаг};
\node[anchor=north west,text width=73mm,align=left,text=Ink,font=\bfseries\fontsize{23}{27}\selectfont] at (10,64) {Пилот в Ярославле};
\node[anchor=north west,text width=72mm,align=left,text=Ink,font=\fontsize{12}{16}\selectfont] at (10,41) {Набираем дежурных мастеров, подключаем звонки и оплату, запускаем первые заявки. Проверяем скорость, точность сметы и качество ремонта.};
\node[anchor=center,inner sep=0] at (119,44) {\includegraphics[width=62mm,height=59mm,keepaspectratio]{../assets/stock/bathroom.jpg}};
\end{scope}\end{tikzpicture}\end{frame}''')

(root / 'main.tex').write_text(preamble + '\\begin{document}\n\n' + '\n\n'.join(slides) + '\n\n\\end{document}\n', encoding='utf-8')
