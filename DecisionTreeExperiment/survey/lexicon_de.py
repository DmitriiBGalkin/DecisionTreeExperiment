class Lexicon:
    # Welcome Screen
    welcome_title = "Willkommen zum Experiment"

    # Section Titles
    profile_info_title = "Profilinformationen"

    # Profile Fields
    loan_amount = "Kreditbetrag"
    loan_duration = "Kreditlaufzeit"
    credit_history = "Kreditwürdigkeit"
    employment_status = "Beschäftigung"
    income = "Einkommen"
    marital_status = "Familienstand"
    assets = "Vermögen"  # Total savings, investments, or property owned
    liabilities = "Verbindlichkeiten"  # Existing financial obligations (e.g., other loans, credit card debt)
    residence = "Wohnstatus"  # Owns home or rents (impacts financial stability)

    # Levels
    credit_history_bad = "Schlecht"
    credit_history_good = "Gut"
    credit_history_excellent = "Hervorragend"

    employment_unemployed = "Arbeitslos"
    employment_stable = "Stabil"

    marital_single = "Ledig"
    marital_married = "Verheiratet"
    marital_divorced = "Geschieden"
    # Outcomes
    approved = "Genehmigt"
    denied = "Abgelehnt"
    # Comparative Terms
    above = "Über"
    below = "Unter"
    between = "Zwischen"
    and_more = "und mehr"
    at_most = "Höchstens"

    # Decision Tree Section
    decision_tree_title = "Verständnis von Entscheidungsbäumen"
    familiarity_with_decision_trees_label = "Wie vertraut sind Sie mit Entscheidungsbäumen?"
    familiarity_with_decision_trees_1 = "Überhaupt nicht vertraut"
    familiarity_with_decision_trees_2 = "Etwas vertraut"
    familiarity_with_decision_trees_3 = "Einigermaßen vertraut"
    familiarity_with_decision_trees_4 = "Sehr vertraut"
    familiarity_with_decision_trees_5 = "Äußerst vertraut"
    survey_title = "Umfrage"

    # Gender
    gender_label = "Welches Geschlecht haben Sie?"
    gender_male = "Mann"
    gender_female = "Frau"
    gender_diverse = "Divers"
    gender_no_answer = "Keine Angabe"

    # Age
    age_label = "Wie alt sind Sie?"
    age_error_message = "Bitte geben Sie ein gültiges Alter zwischen 18 und 100 Jahren ein."

    # Education
    education_label = "Welchen Bildungsabschluss haben Sie? Bitte wählen Sie den höchsten Abschluss, den Sie bisher erreicht haben."
    education_schueler = "Noch Schüler"
    education_hauptschule = "Volks-, Hauptschulabschluss, Quali"
    education_mittlere_reife = "Mittlere Reife, Realschul- oder gleichwertiger Abschluss"
    education_lehre = "Abgeschlossene Lehre"
    education_fachabitur = "Fachabitur, Fachhochschulreife"
    education_abitur = "Abitur, Hochschulreife"
    education_hochschulabschluss = "Fachhochschul-/Hochschulabschluss"
    education_other = "Anderer Abschluss, und zwar:"

    # Serious Participation
    participation_label = (
        "Es wäre sehr hilfreich, wenn Sie uns an dieser Stelle mitteilen könnten, ob Sie ernsthaft teilgenommen haben, "
        "so dass wir Ihre Antworten für unsere wissenschaftliche Analyse nutzen können, oder ob Sie sich nur durchgeklickt haben, "
        "um einen Blick auf die Studie zu werfen.\n"
        "Auch wenn Sie sich nur durchgeklickt haben, werden Sie Ihre Teilnahmeentschädigung erhalten "
        "und es werden Ihnen durch diese Angabe keinerlei Nachteile entstehen!"
    )
    participation_serious = "Ich habe ernsthaft teilgenommen!"
    participation_not_serious = "Ich habe mich nur durchgeklickt, bitte werfen Sie meine Daten weg!"

    # Feedback
    feedback_label = "Möchten Sie zu dieser Studie oder zum besseren Verständnis Ihrer Antworten noch etwas anmerken? "
    "(Ist Ihnen während der Teilnahme an dieser Studie etwas aufgefallen? Waren die Fragen an einer Stelle nicht klar oder war Ihnen die Beantwortung unangenehm? "
    "Bitte schreiben Sie kurz ein paar Stichworte dazu.)"
    state_label = "In welchem Bundesland leben Sie?"

    confidence_level_label = "Wie sicher sind Sie sich mit Ihrer Antwort?"
    confidence_level_1 = "Überhaupt nicht sicher"
    confidence_level_2 = "Leicht sicher"
    confidence_level_3 = "Mäßig sicher"
    confidence_level_4 = "Sehr sicher"
    confidence_level_5 = "Äußerst sicher"

    question_loan_sample1_label = "Basierend auf dem dargestellten Entscheidungsbaum und Ihren Profildaten, wird dieser Kreditantrag genehmigt oder abgelehnt?"
    please_select_correct_answer = "Bitte wählen Sie die korrekte Antwort."