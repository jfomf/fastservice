from pathlib import Path
from PIL import Image
import re

root = Path(__file__).resolve().parent
old = (root / 'main.tex').read_text(encoding='utf-8')
preamble = old.split('\\begin{document}', 1)[0]
preamble = re.sub(r'\\input\{finance_assumptions\.tex\}.*?(?=\\definecolor)', '', preamble, flags=re.S)
preamble = preamble.replace(r'\fontsize{11}{14}\selectfont', r'\fontsize{10}{12.5}\selectfont')

def text_block(heading, body):
    return (rf'{{\bfseries\fontsize{{11.5}}{{14}}\selectfont {heading}}}'
            + r'\par\vspace{2mm}'
            + rf'{{\fontsize{{10.5}}{{13}}\selectfont {body}}}')


def frame(n, label, title, items, image=None, note=None):
    out = [r'\begin{frame}[plain]', rf'\slidebegin{{{label}}}{{{title}}}{{{n}}}']
    if image:
        if image.startswith('../assets/'):
            iw, ih = Image.open(root / image).size
            size = 'width=61mm' if iw / ih < 61 / 40 else 'height=40mm'
            out += [r'\begin{scope}', r'\clip (89,16) rectangle (150,56);',
                    rf'\node[anchor=center,inner sep=0] at (119.5,36) {{\includegraphics[{size}]{{{image}}}}};',
                    r'\end{scope}']
        else:
            out.append(rf'\node[anchor=center,inner sep=0] at (119.5,36) {{\includegraphics[width=61mm,height=40mm,keepaspectratio]{{{image}}}}};')
        content = r'\par\vspace{6mm}'.join(text_block(heading, body) for heading, body in items)
        out.append(rf'\node[anchor=north west,text width=70mm,align=left,inner sep=0] at (10,56) {{{content}}};')
    else:
        for x, (heading, body) in zip((10, 59, 108), items):
            out.append(rf'\node[anchor=north west,text width=42mm,align=left,inner sep=0] at ({x},56) {{{text_block(heading, body)}}};')
    out += [r'\slideend', r'\end{frame}']
    return '\n'.join(out)

slides = []
slides.append(r'''\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay,x=1mm,y=1mm]
\begin{scope}[shift={(current page.south west)}]
\fill[Paper] (0,0) rectangle (160,90);
\node[anchor=west,text=Coral,font=\bfseries\fontsize{12}{14}\selectfont] at (10,84) {Ладно · Ярославль};
\node[anchor=north west,text width=75mm,align=left,text=Ink,font=\bfseries\fontsize{22}{26}\selectfont] at (10,68) {Срочный ремонт\\без поиска мастера};
\node[anchor=north west,text width=70mm,align=left,text=Ink,font=\fontsize{12}{16}\selectfont] at (10,33) {Одна заявка. Цена до выезда. Мы назначим мастера и примем работу.};
\node[anchor=center,inner sep=0] at (119,44) {\includegraphics[width=62mm,height=59mm,keepaspectratio]{../assets/stock/pipe-repair.jpg}};
\end{scope}\end{tikzpicture}\end{frame}''')
slides.append(frame(2,'Проблема','Протёк сифон в воскресенье',[
    ('Клиент','Ищет мастера, сравнивает профили и пишет нескольким людям.'),
    ('Неизвестно','Кто приедет сегодня, сколько стоит ремонт и кто отвечает за результат.')],
    '../assets/stock/tap.jpg','Сценарий бытовой поломки · фото: Pexels'))
slides.append(frame(3,'Сейчас','Клиент сам ведёт заказ',[
    ('Поиск и согласование','Выбирает площадку, пишет мастерам, ждёт цену и время приезда.'),
    ('Приёмка','Сам проверяет работу и решает спорные вопросы.')],
    '../assets/stock/fuse-box.jpg','Типовой путь клиента, а не измеренное время поиска'))
slides.append(frame(4,'Решение','Клиенту достаточно одной заявки',[
    ('Клиент','Описывает поломку, прикладывает фото и оставляет телефон.'),
    ('Ладно','Готовит смету, назначает мастера и ведёт заказ до результата.')],
    'site-home-crop.png','Скриншот действующего frontend-прототипа; звонки пока не подключены'))
slides.append(frame(5,'После заявки','Цель пилота: ответ за 5 минут',[
    ('Первые минуты','Оператор принимает заявку и звонит клиенту.'),
    ('До выезда','Главный мастер готовит смету. Диспетчер назначает исполнителя.')],
    '../assets/stock/worker3.jpg','5 минут — целевой стандарт пилота, не достигнутый показатель'))
slides.append(frame(6,'Цена','Смета до выезда',[
    ('Пример расчёта','Выезд и диагностика 900 ₽; работа 1 600 ₽; материалы 350 ₽.'),
    ('Итого 2 850 ₽','Другие работы согласуют отдельно.')],
    'site-quote-crop.png','Суммы приведены для примера'))
slides.append(frame(7,'Диспетчерская','Мастера назначает диспетчер',[
    ('Назначение','Диспетчер видит фото, адрес, срочность и смету в одном заказе.'),
    ('Отказ исполнителя','Система предлагает следующего подходящего мастера; клиент не начинает поиск заново.')],
    'site-dispatcher-crop.png','Функция переназначения работает в прототипе'))
slides.append(frame(8,'Исполнители','Единый стандарт для мастеров',[
    ('До допуска','Проверяем навыки и обучаем приёмке заказа.'),
    ('На заказе','Заранее знает задачу. После ремонта показывает результат и убирает мусор.')],
    '../assets/stock/socket-work.jpg','Стандарт для запуска пилота; фото: Pexels'))
slides.append(frame(9,'Качество','Приёмка по стандарту',[
    ('После ремонта','Проверка результата с клиентом, фото до и после, уборка.'),
    ('Ответственность','Условия гарантии и итоговая сумма фиксируются в заказе.')],
    '../assets/stock/clean-tools.jpg','Чек-лист — планируемый операционный стандарт'))
slides.append(frame(10,'Прозрачность','Мастер и этапы заказа видны клиенту',[
    ('Карточка мастера','Фото, специализация, предыдущие работы и отзывы.'),
    ('Заказ','Смета, этапы и фотоотчёт.')],
    '../assets/stock/clean-faucet.jpg','Профили и отзывы приведены для примера'))
slides.append(frame(11,'Категории','Сантехника и электрика на старте',[
    ('Сантехника','Течь под раковиной, смеситель, сифон, засор.'),
    ('Электрика','Розетка, свет, диагностика щита.')],
    '../assets/stock/electrician.jpg','Две категории для пилота в Ярославле'))
slides.append(frame(12,'Скорость','Цель пилота: выезд за час',[
    ('При свободном мастере','Диспетчер подтверждает время до выезда.'),
    ('Выходные и праздники','Нужны дежурства и резерв. Если окно занято, сразу назовём доступное время.')],
    '../assets/stock/valves.jpg','Время выезда и дежурства проверим на реальных заказах'))
slides.append(frame(13,'Ярославль','Пилот по районам Ярославля',[
    ('Первый контур','Кировский, Ленинский и Фрунзенский районы: проверяем маршруты и доступность мастеров.'),
    ('Затем','Расширение на Дзержинский и Красноперекопский районы после замера времени выезда.')],
    '../assets/stock/yaroslavl.jpg','Районы — план пилота; фото действительно снято в Ярославле'))
slides.append(frame(14,'Первые заявки','Каналы первых заявок',[
    ('Яндекс Директ','Поисковые объявления по запросам «сантехник срочно Ярославль», «электрик на дом Ярославль».'),
    ('Карты','Карточки сервиса в Яндекс Картах и 2ГИС: услуги, часы работы, зона выезда, телефон.'),
    ('Локально','Объявления Авито по двум категориям и рекомендации после выполненных заказов.')],
    None,'Это план размещения, не действующие кампании'))
slides.append(frame(15,'Роли','Кто ведёт заказ',[
    ('Оператор и диспетчер','Принимают заявку, назначают мастера и следят за временем.'),
    ('Главный мастер','Проверяет смету, обучает исполнителей и контролирует сложные случаи.')],
    '../assets/stock/electric-panel.jpg','Состав команды для пилота формируется; фото: Pexels'))
slides.append(frame(16,'Оплата','Одна оплата за весь заказ',[
    ('До выезда','Клиент получает смету с общей суммой и перечнем работ.'),
    ('После ремонта','Один платёж за заказ. Чек и условия гарантии сохраняются в карточке.')],
    'site-estimate.png','Оплата — часть продуктового плана, не работающая платёжная система'))
slides.append(frame(17,'Пилот','Что измерим в пилоте',[
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
