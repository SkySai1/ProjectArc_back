from flask import Response, request

def privacy_policy():
    """
    Политика конфиденциальности на разных языках.
    """
    lang = request.args.get('lang', 'en')

    privacy_texts = {
        'en': """
        <h1>Privacy Policy</h1>
        <p>Your data is protected. We do not share personal data with third parties.</p>
        <p>This policy describes how we process and store your data.</p>
        <ul>
            <li>We collect data solely to improve service quality.</li>
            <li>Your data is stored on secure servers.</li>
            <li>You can request deletion of your data at any time.</li>
        </ul>
        """,
        'ru': """
        <h1>Политика конфиденциальности</h1>
        <p>Ваши данные защищены. Мы не передаём личные данные третьим лицам.</p>
        <p>Эта политика описывает, как мы обрабатываем и храним ваши данные.</p>
        <ul>
            <li>Мы собираем данные только для улучшения качества сервиса.</li>
            <li>Ваши данные хранятся на защищённых серверах.</li>
            <li>Вы можете запросить удаление ваших данных в любое время.</li>
        </ul>
        """,
        'de': """
        <h1>Datenschutz-Bestimmungen</h1>
        <p>Ihre Daten sind geschützt. Wir geben keine persönlichen Daten an Dritte weiter.</p>
        <p>Diese Richtlinie beschreibt, wie wir Ihre Daten verarbeiten und speichern.</p>
        <ul>
            <li>Wir erheben Daten nur zur Verbesserung der Servicequalität.</li>
            <li>Ihre Daten werden auf sicheren Servern gespeichert.</li>
            <li>Sie können die Löschung Ihrer Daten jederzeit anfordern.</li>
        </ul>
        """,
        'fr': """
        <h1>Politique de confidentialité</h1>
        <p>Vos données sont protégées. Nous ne partageons pas de données personnelles avec des tiers.</p>
        <p>Cette politique décrit comment nous traitons et stockons vos données.</p>
        <ul>
            <li>Nous collectons des données uniquement pour améliorer la qualité du service.</li>
            <li>Vos données sont stockées sur des serveurs sécurisés.</li>
            <li>Vous pouvez demander la suppression de vos données à tout moment.</li>
        </ul>
        """,
        'zh': """
        <h1>隐私政策</h1>
        <p>您的数据是安全的。我们不会与第三方分享个人数据。</p>
        <p>本政策描述了我们如何处理和存储您的数据。</p>
        <ul>
            <li>我们仅收集数据以提高服务质量。</li>
            <li>您的数据存储在安全的服务器上。</li>
            <li>您可以随时请求删除您的数据。</li>
        </ul>
        """
    }

    privacy_text = privacy_texts.get(lang, privacy_texts['en'])
    return Response(privacy_text, content_type='text/html')