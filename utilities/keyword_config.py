
company_patterns = {
    "amazon": {
        "include": [
            r"\bamazon\b", "aws", "prime_video", "kindle",
            r"\balexa\b", "jeff_bezos"
        ],
        "exclude": ["rainforest", "river", "basin", "jungle", "mythology"]
    },
    "google": {
        "include": ["google", "youtube", "gmail", "android", "alphabet_inc", "sundar_pichai"],
        "exclude": []
    },
    "apple": {
        "include": ["apple_inc", "iphone", "macbook", "ipad", "tim_cook", "ios", "macos", "steve_jobs"],
        "exclude": ["pineapple","fruit", "tree", "pie", "cider", "juice", "orchard"]
    },
    "facebook": {
        "include": ["meta_platforms","meta", "facebook", "instagram", "whatsapp", "mark_zuckerberg"],
        "exclude": ["metadata", "metaphor", "metamorphosis", "metabolism", "metaphysics"]
    },
    "microsoft": {
        "include": ["microsoft", "xbox", "azure", "satya_nadella", "windows_10", "windows_11"],
        "exclude": []
    }
}
