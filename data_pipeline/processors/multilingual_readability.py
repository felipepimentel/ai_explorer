import textstat
from langdetect import detect

class MultilingualReadabilityAnalyzer:
    def __init__(self):
        self.analyzers = {
            'en': textstat.textstat,
            'es': textstat.textstat_es,
            'de': textstat.textstat_de,
            'fr': textstat.textstat_fr,
            'it': textstat.textstat_it,
            'nl': textstat.textstat_nl,
            'ru': textstat.textstat_ru
        }

    def analyze_readability(self, text):
        lang = detect(text)
        analyzer = self.analyzers.get(lang, textstat.textstat)
        
        return {
            'language': lang,
            'flesch_reading_ease': analyzer.flesch_reading_ease(text),
            'flesch_kincaid_grade': analyzer.flesch_kincaid_grade(text),
            'smog_index': analyzer.smog_index(text),
            'coleman_liau_index': analyzer.coleman_liau_index(text),
            'automated_readability_index': analyzer.automated_readability_index(text),
            'dale_chall_readability_score': analyzer.dale_chall_readability_score(text),
            'difficult_words': analyzer.difficult_words(text),
            'linsear_write_formula': analyzer.linsear_write_formula(text),
            'gunning_fog': analyzer.gunning_fog(text),
            'text_standard': analyzer.text_standard(text)
        }

# Uso:
# analyzer = MultilingualReadabilityAnalyzer()
# readability_scores = analyzer.analyze_readability("This is a sample text to analyze for readability.")