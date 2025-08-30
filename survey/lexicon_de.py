class Lexicon:
    # Welcome Screen
    welcome_title = "Willkommen zum Experiment"

    # Section Titles
    profile_info_title = "Profilinformationen"

    # Profile Fields
    loan_amount = "Kreditbetrag"
    loan_duration = "Kreditlaufzeit"
    credit_history = "Kreditwürdigkeit"
    employment_status = "Berufstätigkeit"
    income = "Gehalt"
    marital_status = "Familienstand"
    assets = "Vermögen"  # Total savings, investments, or property owned
    liabilities = "Verbindlichkeiten"  # Existing financial obligations (e.g., other loans, credit card debt)
    residence = "Wohnstatus"  # Owns home or rents (impacts financial stability)

    # Levels
    credit_history_bad = "Schlecht"
    credit_history_good = "Gut"
    credit_history_excellent = "Exzellent"

    employment_unemployed = "Arbeitslos"
    employment_stable = "Berufstätig"
    residence_rented = "Miete"
    residence_mortgage = "Hypothek"
    residence_homeowner = "Eigentümer"

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
    or_oder = "oder"
    not_nicht = "Nicht"
    # Decision Tree Section
    decision_tree_title = "Verständnis von Entscheidungsbäumen"
    familiarity_with_decision_trees_label = "Sind Sie in Ihrem persönlichen, akademischen oder beruflichen Umfeld bereits mit Entscheidungsbäumen zur Abbildung von Entscheidungsprozessen in Berührung gekommen?"

    familiarity_with_decision_trees_1 = "Überhaupt nicht"
    familiarity_with_decision_trees_2 = "Selten"
    familiarity_with_decision_trees_3 = "Gelegentlich"
    familiarity_with_decision_trees_4 = "Häufig"
    familiarity_with_decision_trees_5 = "Sehr häufig"

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
    education_prescreener= "Welchen höchsten Bildungsabschluss Sie erworben haben?"
    education_label = "Welchen Bildungsabschluss haben Sie? Bitte wählen Sie den höchsten Abschluss, den Sie bisher erreicht haben."

    education_schueler = "Noch Schüler"
    education_hauptschule = "Volks- oder Hauptschulabschluss (inkl. Quali)"
    education_mittlere_reife = "Mittlere Reife / Realschulabschluss oder gleichwertig"
    education_lehre = "Abgeschlossene Berufsausbildung / Lehre"
    education_fachabitur = "Fachabitur / Fachhochschulreife"
    education_abitur = "Allgemeine Hochschulreife / Abitur"
    education_bachelor = "Bachelorabschluss"
    education_master = "Masterabschluss / Diplom / Magister / Staatsexamen"
    education_phd = "Promotion / Doktortitel"
    education_other = "Anderer Abschluss (bitte angeben)"


    study_label = "Was ist (oder war) Ihr Studienfach?"
    study_none = "Kein Studium / Nicht zutreffend"
    study_engineering = "Ingenieurwissenschaften"
    study_computer_science = "Informatik / Informationstechnologie"
    study_mathematics = "Mathematik / Statistik"
    study_natural_sciences = "Naturwissenschaften (z. B. Physik, Chemie, Biologie)"
    study_medicine = "Medizin / Gesundheitswissenschaften"
    study_economics = "Wirtschaftswissenschaften / Betriebswirtschaftslehre"
    study_law = "Rechtswissenschaften"
    study_social_sciences = "Sozialwissenschaften / Politikwissenschaft / Soziologie"
    study_education = "Erziehungswissenschaft / Pädagogik"
    study_humanities = "Geisteswissenschaften / Kunst / Sprachen"
    study_other = "Anderes Fach (bitte angeben)"
    study_other_label = "Falls anderes Fach, bitte angeben:"

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


    confidence_level_label = "Auf einer Skala von 0 bis 100: Wie sicher sind Sie sich, dass Ihre Antwort zur Vergabe des Kredits korrekt ist?"
    value_label_prefix = "Wert:"
    value_label_suffix = "/100"
    move_slider_warning = "Bitte verschieben Sie den Regler, um Ihre Sicherheit anzugeben."

    question_loan_sample1_label = "Wird dieser Kreditantrag basierend auf dem Entscheidungsbaum und Ihren persönlichen Daten genehmigt oder abgelehnt?"
    please_select_correct_answers = "Bitte wählen Sie die richtigen Antworten aus."
    attention_check_label = "Dies ist eine Aufmerksamkeitsprüfung. Bitte wählen Sie entsprechend der Anweisung die linke Antwort aus (Genehmigt)."
    attention_check_label_confidence = "Dies ist eine Aufmerksamkeitsfrage. Bitte wählen Sie die äußerste rechte Option (Sehr sicher)."

    subjective_social_status_label = "Stellen Sie sich vor, diese Leiter repräsentiert die gesellschaftliche Stellung von Menschen. Oben stehen diejenigen, denen es am besten geht – sie haben das meiste Geld, die beste Bildung und die angesehensten Berufe. Unten stehen diejenigen, denen es am schlechtesten geht. Wo würden Sie sich selbst auf dieser Leiter einordnen?"
    income_band_label = "Wie hoch ist Ihr ungefähres Jahreseinkommen (vor Steuern)?"
    income_band_1 = "Weniger als 10.000 €"
    income_band_2 = "10.000 € – 19.999 €"
    income_band_3 = "20.000 € – 29.999 €"
    income_band_4 = "30.000 € – 39.999 €"
    income_band_5 = "40.000 € – 49.999 €"
    income_band_6 = "50.000 € – 59.999 €"
    income_band_7 = "60.000 € – 69.999 €"
    income_band_8 = "70.000 € oder mehr"

    feedback_label_SF = "Bitte hinterlassen Sie Kommentare, Feedback oder Verbesserungsvorschläge oder teilen Sie uns mit, falls Sie Fehler im Experiment gefunden haben."

    # Entscheidungsbaumteile
    root_node = "Wurzelknoten"
    label_root_node = "Start des Entscheidungsprozesses"

    decision_node = "Entscheidungsknoten"
    label_decision_node = "Regel oder Frage"
    branch = "Zweig"
    branch_condition = "Bedingung"

    leaf_node = "Blattknoten"
    label_leaf_node = "Endgültige Entscheidung"

    salary = "Gehalt"
    no_education = "Ohne beruflichen Bildungsabschluss"
    vocational_education = "Lehre/Berufsausbildung im dualen System"
    higher_education = "Universitäts- oder Hochschulbildung"