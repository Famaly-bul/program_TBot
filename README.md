 <h1>Telegram Task Planner Bot</h1>
  <div class="section">
    <p>
      <strong>Telegram Task Planner Bot</strong> — это бот для планирования задач и мест для свидания по датам прямо в Telegram.<br>
      Задачи сохраняются в файл <code>tasks.json</code> и доступны только вам.
    </p>
  </div>

  <div class="section">
    <h2>Возможности</h2>
    <ul>
      <li><code>/start</code> — приветствие</li>
      <li><code>/help</code> — справка по командам</li>
      <li><code>/add &lt;дата&gt; &lt;задача&gt;</code> — добавить задачу на выбранную дату</li>
      <li><code>/show &lt;дата&gt; [страница]</code> — показать задачи на дату (с пагинацией)</li>
      <li><code>/showall [страница]</code> — показать все задачи (с пагинацией)</li>
      <li><code>/random &lt;дата&gt;</code> — добавить случайное место для свидания на выбранную дату</li>
      <li><code>/delete &lt;дата&gt; &lt;номер_задачи&gt;</code> — удалить задачу по номеру</li>
      <li><code>/edit &lt;дата&gt; &lt;номер_задачи&gt; &lt;новый_текст&gt;</code> — редактировать задачу</li>
      <li><code>/done &lt;дата&gt; &lt;номер_задачи&gt;</code> — отметить задачу выполненной</li>
      <li><code>/find &lt;текст&gt;</code> — поиск задач по тексту</li>
      <li><code>/stats</code> — статистика задач</li>
      <li><code>/export</code> — экспорт всех задач в файл</li>
    </ul>
  </div>

  <div class="section">
    <h2>Формат даты</h2>
    <ul>
      <li><code>ДД.ММ</code></li>
      <li><code>ДД.ММ.ГГГГ</code></li>
    </ul>
  </div>
  
  <div class="section">
    <h2>Хранение задач</h2>
    <p>Все задачи сохраняются в файл <code>tasks.json</code> автоматически при добавлении, удалении или изменении.</p>
    <p>Каждый пользователь видит только свои задачи.</p>
  </div>

  <div class="section">
    <h2>Безопасность</h2>
    <ul>
      <li>Токен Telegram-бота хранится в переменной окружения и не должен попадать в публичные репозитории.</li>
      <li>Файл <code>.env</code> рекомендуется добавить в <code>.gitignore</code>.</li>
    </ul>
  </div>

  <div class="section">
    <h2>Пример использования</h2>
    <ul>
      <li>Добавить задачу:<br>
        <code>/add 21.09 Купить цветы</code>
      </li>
      <li>Показать задачи на дату:<br>
        <code>/show 21.09</code>
      </li>
      <li>Добавить случайное место:<br>
        <code>/random 21.09</code>
      </li>
      <li>Удалить задачу:<br>
        <code>/delete 21.09 1</code>
      </li>
      <li>Редактировать задачу:<br>
        <code>/edit 21.09 1 Новый текст задачи</code>
      </li>
      <li>Отметить задачу выполненной:<br>
        <code>/done 21.09 1</code>
      </li>
      <li>Найти задачу:<br>
        <code>/find цветы</code>
      </li>
      <li>Статистика:<br>
        <code>/stats</code>
      </li>
      <li>Экспорт задач:<br>
        <code>/export</code>
      </li>
    </ul>
  </div>

  <div class="section">
    <h2>Автор</h2>
    <p><b>Онуприенко Михаил</b></p>
  </div>
</body>
</html>
