class Lexicon:
    welcome_title = "Welcome to the Experiment"
    # Section Titles
    profile_info_title = "Profile Information"
    loan_amount = "Loan Amount"
    loan_duration = "Loan Duration"
    credit_history = "Credit History"
    employment_status = "Employment"
    income = "Income"
    marital_status = "Marital Status"
    assets = "Assets"  # Total savings, investments, or property owned
    liabilities = "Liabilities"  # Existing financial obligations (e.g., other loans, credit card debt)
    residence = "Residence"  # Owns home or rents (impacts financial stability)
    # Levels
    credit_history_bad = "Bad"
    credit_history_good = "Good"
    credit_history_excellent = "Excellent"
    employment_unemployed = "Unemployed"
    employment_stable = "Stable"
    marital_single = "Single"
    marital_married = "Married"
    marital_divorced = "Divorced"
    # Comparative Terms
    above = "Above"
    below = "Below"
    between = "Between"
    at_least = "At least"
    at_most = "At most"
    and_more = "and more"
    approved = "Approved"
    denied = "Denied"
    #Decision Tree Question
    decision_tree_title = "Understanding Decision Trees"
    familiarity_with_decision_trees_label = "Have you previously encountered decision trees or similar diagrammatic tools (e.g., flowcharts) for representing decision-making processes in your personal, educational, or professional life?"
    familiarity_with_decision_trees_1 = "Not at all"
    familiarity_with_decision_trees_2 = "Rarely"
    familiarity_with_decision_trees_3 = "Occasionally"
    familiarity_with_decision_trees_4 = "Frequently"
    familiarity_with_decision_trees_5 = "Very frequently"

    survey_title = "Survey"
    or_oder = "or"
    not_nicht = "Not"

    residence_rented = "Rented"
    residence_mortgage = "Mortgage"
    residence_homeowner = "Homeowner"

    # Gender
    gender_label = "What is your gender?"
    gender_male = "Man"
    gender_female = "Woman"
    gender_diverse = "Diverse"
    gender_no_answer = "Prefer not to say"

    # Age
    age_label = "How old are you?"
    age_error_message = "Please enter a valid age between 18 and 100."

    # Education
    education_label = "What is the highest level of education you have completed?"

    education_schueler = "Still in school"
    education_hauptschule = "Lower secondary education (e.g., Hauptschule)"
    education_mittlere_reife = "Intermediate secondary education (e.g., Realschule or equivalent)"
    education_lehre = "Completed vocational training / apprenticeship"
    education_fachabitur = "Advanced technical college entrance qualification"
    education_abitur = "General higher education entrance qualification (Abitur)"
    education_bachelor = "Bachelor’s degree"
    education_master = "Master’s degree / Diploma / Magister / State examination"
    education_phd = "Doctorate / PhD"
    education_other = "Other (please specify)"

    education_currently_a_student_label = "Are you currently a pupil or a student?"
    # Yes/No
    yes = "Yes"
    no = "No"


    study_label = "What is your (current or past) field of study?"
    study_none = "I did not study / not applicable"
    study_engineering = "Engineering"
    study_computer_science = "Computer Science / Information Technology"
    study_mathematics = "Mathematics / Statistics"
    study_natural_sciences = "Natural Sciences (e.g., Physics, Chemistry, Biology)"
    study_medicine = "Medicine / Health Sciences"
    study_economics = "Economics / Business Administration"
    study_law = "Law"
    study_social_sciences = "Social Sciences / Political Science / Sociology"
    study_education = "Education / Pedagogy"
    study_humanities = "Humanities / Arts / Languages"
    study_other = "Other (please specify)"
    study_other_label = "If other, please specify:"

    # Serious Participation
    participation_label = (
        "It would be very helpful if you could tell us whether you participated seriously, "
        "so that we can use your answers for our scientific analysis, or if you just clicked through the study to get an overview.\n"
        "Even if you only clicked through, you will still receive your participation compensation, "
        "and there will be no disadvantages for you!"
    )
    participation_serious = "I participated seriously!"
    participation_not_serious = "I just clicked through, please discard my data!"

    # Feedback
    feedback_label = "Would you like to provide feedback on this study or help us understand your answers better? "
    "(Did anything stand out during the study? Were any questions unclear or uncomfortable? "
    "Please write a few brief notes.)"
    state_label = "Which federal state do you live in?"

    confidence_level_label = "On the scale from 0 (not confident at all) to 100 (absolutely confident), how confident are you in your answer?"
    value_label_prefix = "Value:"
    value_label_suffix = "/100"
    move_slider_warning = "Please move the slider to indicate your confidence."

    question_loan_sample1_label = "Based on the presented decision tree and your profile information, would this loan be approved or denied?"
    please_select_correct_answers = "Please select the correct answers."
    attention_check_label = "This is an attention check. Based on the instructions, please select the left answer (Approved)."
    attention_check_label_confidence = "This is an attention check. Please select the rightmost option (Extremely confident)."

    subjective_social_status_label = "Think of this ladder as representing where people stand in society. At the top are the people who are best off—those who have the most money, education, and respected jobs. At the bottom are the people who are worst off. Where would you place yourself on this ladder?"
    income_band_label = "What is your approximate yearly income (before taxes)?"
    income_band_1 = "Less than €10,000"
    income_band_2 = "€10,000 – €19,999"
    income_band_3 = "€20,000 – €29,999"
    income_band_4 = "€30,000 – €39,999"
    income_band_5 = "€40,000 – €49,999"
    income_band_6 = "€50,000 – €59,999"
    income_band_7 = "€60,000 – €69,999"
    income_band_8 = "€70,000 or more"

    feedback_label_SF = "Please leave any comments, feedback, suggestions, or let us know if you found any mistakes in the experiment."
    # Trust in Decision Trees
    trust_decision_trees_label = (
        "Based on your experience with decision trees in this study, "
        "to what extent would you trust decision trees as an explanation for loan application decisions?"
    )

    trust_decision_trees_1 = "Not at all"
    trust_decision_trees_2 = "Slightly"
    trust_decision_trees_3 = "Moderately"
    trust_decision_trees_4 = "Quite a lot"
    trust_decision_trees_5 = "Completely"
