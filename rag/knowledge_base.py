"""
Knowledge base for DermaScan ML chatbot RAG system.
20 documents covering photo tips, result interpretation,
ABCD rule, medical guidance, and model explanation.
"""

DOCUMENTS = [

    # ── Photo tips ─────────────────────────────────────────────────────────────
    {
        "id": "photo_lighting",
        "title": "How to get the best lighting for your scan",
        "content": (
            "Good lighting is the single most important factor for a quality scan. "
            "Use natural daylight whenever possible — go near a window or step outside. "
            "Avoid direct sunlight, which creates harsh shadows and reflections. "
            "Indoor lighting from a lamp directly above or beside the lesion also works well. "
            "Never use flash — it washes out color variations that the model uses to detect abnormalities. "
            "If you notice a bright glare or white spot on the lesion in the preview, "
            "adjust your angle slightly until the reflection disappears."
        ),
        "tags": ["photo", "tips", "lighting", "quality"],
    },
    {
        "id": "photo_distance",
        "title": "Ideal distance and focus for scanning a lesion",
        "content": (
            "Hold your phone approximately 8–12 cm (3–5 inches) from the lesion. "
            "This distance fills the frame with the lesion while keeping surrounding skin visible for context. "
            "Tap the lesion on your screen to force the camera to focus on it — "
            "this is the most important step to avoid blurry images. "
            "Keep the phone as steady as possible; rest your elbow on a surface if needed. "
            "The lesion should occupy at least 30% of the image frame. "
            "If you can see individual hairs clearly, you are at a good distance."
        ),
        "tags": ["photo", "tips", "distance", "focus", "quality"],
    },
    {
        "id": "photo_preparation",
        "title": "Preparing the skin before taking a scan",
        "content": (
            "Before scanning, gently clean the area with a mild soap and pat dry. "
            "Remove any makeup, sunscreen, or creams from the skin around the lesion — "
            "these can alter the color and texture the model analyses. "
            "Do not stretch or press the skin, as this changes the appearance of borders. "
            "If the lesion is in a hard-to-reach location, ask someone else to take the photo "
            "so you can hold the skin flat. "
            "For body hair covering the lesion, you may gently wet the hair to flatten it, "
            "but avoid shaving immediately before scanning as this can cause redness."
        ),
        "tags": ["photo", "tips", "preparation", "skin", "quality"],
    },
    {
        "id": "photo_angle",
        "title": "Best angle and framing for accurate results",
        "content": (
            "Always photograph the lesion straight on (perpendicular to the skin surface), "
            "not at an angle. Angled shots distort the shape and make asymmetry analysis unreliable. "
            "Centre the lesion in the frame with a small border of normal skin around it — "
            "this helps the model understand where the lesion ends. "
            "Take multiple photos from slightly different angles and submit the sharpest one. "
            "Avoid zooming in digitally; move the phone closer instead, as digital zoom reduces quality. "
            "If your phone has a macro or portrait mode, use it for close-up lesion photography."
        ),
        "tags": ["photo", "tips", "angle", "framing", "quality"],
    },

    # ── ABCD Rule ─────────────────────────────────────────────────────────────
    {
        "id": "abcd_asymmetry",
        "title": "ABCD Rule — A is for Asymmetry",
        "content": (
            "Asymmetry is the first letter of the ABCD rule for evaluating skin lesions. "
            "A benign mole is typically symmetrical — if you draw a line through the middle, "
            "both halves look the same. "
            "A potentially cancerous lesion is often asymmetrical: one half looks different from the other. "
            "Our model extracts asymmetry features using HOG (Histogram of Oriented Gradients) descriptors, "
            "which capture the directional structure of the lesion. "
            "A high asymmetry score increases the model's probability estimate for malignancy."
        ),
        "tags": ["abcd", "asymmetry", "model", "features"],
    },
    {
        "id": "abcd_border",
        "title": "ABCD Rule — B is for Border",
        "content": (
            "Border irregularity is the B in the ABCD rule. "
            "Benign lesions typically have smooth, well-defined borders. "
            "Malignant lesions often have irregular, ragged, notched, or blurred edges. "
            "The border may appear to bleed or fade into the surrounding skin. "
            "When photographing a lesion to check its border, ensure the entire lesion "
            "fits within the frame with visible healthy skin around it — "
            "cutting off the edge makes border analysis impossible for the model."
        ),
        "tags": ["abcd", "border", "model", "features"],
    },
    {
        "id": "abcd_color",
        "title": "ABCD Rule — C is for Color",
        "content": (
            "Color variation is the C in the ABCD rule. "
            "A benign mole is usually a single uniform shade of brown or tan. "
            "Warning signs include multiple colours within the same lesion: "
            "shades of brown, black, red, white, or blue. "
            "The model analyses color variation using RGB channel histograms extracted from the HOG features. "
            "This is why good lighting is critical — poor lighting changes perceived colour "
            "and can mask real variation or create false variation. "
            "Natural daylight gives the most accurate colour representation."
        ),
        "tags": ["abcd", "color", "model", "features"],
    },
    {
        "id": "abcd_diameter",
        "title": "ABCD Rule — D is for Diameter",
        "content": (
            "Diameter is the D in the ABCD rule. "
            "Melanomas are usually larger than 6 mm (about the size of a pencil eraser) when diagnosed. "
            "However, they can be smaller when first detected, so size alone is not sufficient. "
            "To give the model a reference, include a ruler or a known object (like a coin) "
            "at the edge of the frame in a second photo. "
            "Any lesion growing rapidly in size — even if small — should be evaluated by a dermatologist. "
            "The E (Evolution) is sometimes added: any change in size, shape, or color is a warning sign."
        ),
        "tags": ["abcd", "diameter", "size", "evolution"],
    },

    # ── Result interpretation ─────────────────────────────────────────────────
    {
        "id": "result_cancerous",
        "title": "What a 'Potentially Cancerous' result means",
        "content": (
            "A 'Potentially Cancerous' result means the model found features in your image "
            "that are statistically associated with malignant skin lesions in the HAM10000 training dataset. "
            "This is a flag for clinical follow-up, not a diagnosis. "
            "The model is tuned with a low threshold (21.4%) to catch as many potential cancers as possible, "
            "which means it will sometimes flag benign lesions too (false positives). "
            "You should book an appointment with a dermatologist within 1–2 weeks. "
            "Do not panic — the majority of flagged lesions turn out to be benign after professional review. "
            "Bring the probability score and photo to your appointment."
        ),
        "tags": ["result", "cancerous", "positive", "action"],
    },
    {
        "id": "result_non_cancerous",
        "title": "What a 'Non-Cancerous' result means",
        "content": (
            "A 'Non-Cancerous' result means the model did not detect strong indicators of malignancy. "
            "The lesion's features — asymmetry, border, color, and texture — appear consistent "
            "with benign skin conditions in the HAM10000 dataset. "
            "However, this is not a medical clearance. "
            "Continue to monitor the lesion monthly using the ABCD rule. "
            "If you notice any changes — new colours, change in size, bleeding, or itching — "
            "rescan immediately and see a dermatologist regardless of the model result. "
            "Annual skin check-ups with a professional are recommended for everyone."
        ),
        "tags": ["result", "non-cancerous", "negative", "monitoring"],
    },
    {
        "id": "result_confidence",
        "title": "Understanding the confidence score and probability",
        "content": (
            "The probability score (P(cancerous)) represents how likely the model thinks the lesion is malignant, "
            "on a scale from 0.0 to 1.0. "
            "Our decision threshold is 0.214 — any score above this is classified as 'potentially cancerous'. "
            "This threshold was chosen using Youden's J statistic to maximise both sensitivity and specificity, "
            "with a deliberate bias toward sensitivity (catching real cancers). "
            "A score of 0.34 means 34% cancer probability — above threshold, so flagged. "
            "A score of 0.10 means 10% — below threshold, classified as non-cancerous. "
            "Higher scores warrant more urgency in seeking professional review."
        ),
        "tags": ["result", "confidence", "probability", "threshold", "score"],
    },

    # ── Medical guidance ──────────────────────────────────────────────────────
    {
        "id": "see_doctor_urgent",
        "title": "When to see a doctor immediately",
        "content": (
            "Seek immediate medical attention if a lesion shows any of these signs: "
            "rapid change in size over days or weeks; "
            "bleeding without injury; "
            "ulceration (open sore that doesn't heal); "
            "satellite lesions appearing nearby; "
            "pain, tenderness, or itching in the lesion; "
            "or a nail lesion with a dark streak extending to the cuticle (subungual melanoma). "
            "Do not wait for a model result in these cases — go directly to a dermatologist or emergency room. "
            "Early melanoma is nearly 100% curable; advanced melanoma is much harder to treat."
        ),
        "tags": ["urgent", "doctor", "emergency", "symptoms", "warning"],
    },
    {
        "id": "dermatologist_visit",
        "title": "What to expect at a dermatologist appointment",
        "content": (
            "A dermatologist will examine your lesion using a dermatoscope — a magnifying tool with polarised light "
            "that reveals subsurface structures invisible to the naked eye. "
            "If suspicious, they may perform a biopsy: a small tissue sample taken under local anaesthetic. "
            "Results from a biopsy take 1–2 weeks. "
            "Bring the DermaScan result, the probability score, and the original photo to your appointment — "
            "this gives the doctor useful context. "
            "If the lesion is benign, the dermatologist may recommend monitoring, "
            "removal for cosmetic reasons, or no action. "
            "If malignant, they will discuss surgical excision and further treatment options."
        ),
        "tags": ["dermatologist", "appointment", "biopsy", "what to expect"],
    },
    {
        "id": "self_examination",
        "title": "How to perform a monthly skin self-examination",
        "content": (
            "Perform a full skin self-examination once a month, ideally after a shower in good lighting. "
            "Use a full-length mirror and a hand mirror for hard-to-see areas. "
            "Check your scalp by parting the hair with a comb. "
            "Examine the front and back of your body, including underarms. "
            "Check both sides of your arms, between fingers, and under your nails. "
            "Examine the front, sides, and back of your legs, and the soles of your feet. "
            "Use the DermaScan app to photograph any lesion that looks new, "
            "has changed, or matches the ABCD criteria. "
            "Keep a photo log over time — changes are easier to spot when you compare."
        ),
        "tags": ["self-examination", "monthly", "monitoring", "prevention"],
    },
    {
        "id": "risk_factors",
        "title": "Risk factors for skin cancer",
        "content": (
            "The main risk factors for skin cancer include: "
            "fair skin with tendency to burn rather than tan; "
            "history of sunburns, especially in childhood; "
            "excessive UV exposure from sun or tanning beds; "
            "more than 50 moles, or having atypical (dysplastic) moles; "
            "personal or family history of skin cancer; "
            "weakened immune system; "
            "exposure to radiation or certain chemicals. "
            "People with darker skin tones have lower risk but are not immune — "
            "melanoma in darker-skinned people is often diagnosed later, making early screening important for everyone. "
            "Wearing SPF 30+ sunscreen daily is the most effective prevention."
        ),
        "tags": ["risk", "prevention", "sunscreen", "uv", "moles"],
    },

    # ── Model & technical ─────────────────────────────────────────────────────
    {
        "id": "model_explanation",
        "title": "How the DermaScan ML model works",
        "content": (
            "DermaScan ML uses a Random Forest classifier trained on the HAM10000 dataset. "
            "When you submit an image, the model: "
            "1. Resizes it to 128×128 pixels; "
            "2. Extracts HOG (Histogram of Oriented Gradients) features — these capture edges, "
            "textures, and structural patterns in 9 directions across 16×16 pixel cells; "
            "3. Combines HOG features with your metadata (age, sex, localization); "
            "4. Passes the combined feature vector through 500 decision trees; "
            "5. Each tree votes cancerous or non-cancerous; "
            "6. The vote proportion gives P(cancerous); "
            "7. If P(cancerous) ≥ 0.214, the lesion is flagged. "
            "The model achieves 79.4% cancer recall and 76.3% AUC on the test set."
        ),
        "tags": ["model", "technical", "hog", "random forest", "how it works"],
    },
    {
        "id": "ham10000_dataset",
        "title": "About the HAM10000 dataset",
        "content": (
            "HAM10000 (Human Against Machine with 10,000 training images) is a benchmark dataset "
            "of 10,015 dermatoscopic images of pigmented skin lesions collected from clinics in Austria and Australia. "
            "It contains 7 diagnostic categories: "
            "melanoma (mel), basal cell carcinoma (bcc), actinic keratoses (akiec), "
            "melanocytic nevi (nv), benign keratosis-like lesions (bkl), "
            "dermatofibroma (df), and vascular lesions (vasc). "
            "For DermaScan, we map these to binary: "
            "mel + bcc + akiec = cancerous (1,954 images); "
            "nv + bkl + df + vasc = non-cancerous (8,061 images). "
            "The model was trained on 70% (7,009 images) and tested on 30% (3,006 images)."
        ),
        "tags": ["dataset", "ham10000", "training", "categories"],
    },
    {
        "id": "model_limitations",
        "title": "Limitations of the DermaScan model",
        "content": (
            "DermaScan ML has several important limitations you should understand: "
            "1. It was trained on dermatoscopic images — professional close-up photos with polarised light. "
            "Smartphone photos have lower quality and different lighting, which affects accuracy. "
            "2. The model cannot analyse lesions on mucous membranes, eyes, or under nails. "
            "3. It performs best on lesions larger than 5mm with clear borders. "
            "4. Very dark skin tones are underrepresented in the HAM10000 dataset, "
            "which may reduce accuracy for these populations. "
            "5. Overall test accuracy is 63.4% — the low threshold means many benign lesions are flagged. "
            "This is intentional: missing a cancer is far worse than a false alarm."
        ),
        "tags": ["limitations", "accuracy", "bias", "model"],
    },
    {
        "id": "benign_conditions",
        "title": "Common benign skin conditions that may be flagged",
        "content": (
            "Several harmless conditions can trigger a 'potentially cancerous' result because they share "
            "visual features with malignant lesions: "
            "Seborrhoeic keratosis — waxy, wart-like growths that can appear dark and irregular; "
            "Dermatofibroma — firm, slightly raised bumps often on legs; "
            "Haemangioma — bright red vascular lesions; "
            "Blue naevus — deeply pigmented, bluish moles; "
            "Ink-spot lentiginous naevus — very dark, irregular moles. "
            "If you receive a positive result, do not assume the worst — "
            "the most common outcome of a dermatologist visit after a flagged scan "
            "is confirmation that the lesion is benign."
        ),
        "tags": ["benign", "false positive", "seborrheic keratosis", "conditions"],
    },
    {
        "id": "metadata_importance",
        "title": "Why age, sex, and body location improve accuracy",
        "content": (
            "The model uses three pieces of patient metadata alongside the image: age, sex, and body location. "
            "These matter because skin cancer risk varies significantly: "
            "melanoma is more common on the back in men and on the legs in women; "
            "basal cell carcinoma predominantly affects sun-exposed areas (face, neck, scalp); "
            "acral lentiginous melanoma (on hands, feet, nails) is more common in darker-skinned populations. "
            "Older age increases the probability of malignancy for the same visual appearance. "
            "Providing accurate metadata improves prediction by approximately 4%. "
            "If you are unsure about the body location, choose the closest match from the list."
        ),
        "tags": ["metadata", "age", "sex", "location", "accuracy"],
    },
    {
        "id": "after_positive_result",
        "title": "Step-by-step guide after a positive (cancerous) result",
        "content": (
            "If DermaScan flags your lesion as potentially cancerous, follow these steps: "
            "1. Do not panic — most flagged lesions are benign. "
            "2. Take a high-quality photo of the lesion with a ruler for scale. "
            "3. Book an appointment with a dermatologist within 1–2 weeks. "
            "4. Mention that you used a screening app and show them the result and probability score. "
            "5. In the meantime, avoid scratching, squeezing, or irritating the lesion. "
            "6. Do not apply any creams, oils, or treatments without medical advice. "
            "7. Monitor for any rapid changes — if the lesion grows quickly, bleeds, or ulcerates, "
            "seek urgent medical attention. "
            "8. Protect the area from UV with clothing or SPF 50+ sunscreen."
        ),
        "tags": ["after result", "steps", "positive", "action plan"],
    },
]
