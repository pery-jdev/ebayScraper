import translators as ts
import logging

from translatepy.translators.google import GoogleTranslate
from typing import Optional, Literal

class MultiTranslator(object):
    def __init__(self, translator: Literal["translators", "translatepy"] = "translatepy"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.translator_type = translator
        self.google_translator = GoogleTranslate() if translator == "translatepy" else None
        
    def translate_text(self, text: str, to_lang: str="en", from_lang: str = "auto") -> Optional[str]:
        """Translate text using selected translator"""
        try:
            if self.translator_type == "translatepy":
                result = self.google_translator.translate(text, destination_language=to_lang).result
                self.logger.info("Successfully translated using GoogleTranslate")
                return result
            else:
                # _ = ts.preaccelerate_and_speedtest()  # Optional. Caching sessions in advance, which can help improve access speed.
                result = ts.translate_text(text, to_language=to_lang, from_language=from_lang, translator='google')
                self.logger.info("Successfully translated using translators")
                return result
        except Exception as e:
            self.logger.error(f"Translation failed: {e}")
            # Try fallback to other library
            return self._fallback_translate(text, to_lang, from_lang)
    
    def _fallback_translate(self, text: str, to_lang: str, from_lang: str) -> Optional[str]:
        """Fallback to alternative translator if primary fails"""
        try:
            if self.translator_type == "translatepy":
                self.logger.warning("Falling back to translators library")
                return ts.translate_text(text, to_language=to_lang, from_language=from_lang)
            else:
                self.logger.warning("Falling back to GoogleTranslate")
                return GoogleTranslate().translate(text, to_lang)
        except Exception as e:
            self.logger.error(f"Fallback translation failed: {e}")
            return None

    def translate_html(self, html: str, to_lang: str, from_lang: str = "auto") -> Optional[str]:
        """Translate HTML content (only supported by translators library)"""
        try:
            if self.translator_type == "translatepy":
                self.logger.warning("HTML translation not supported by GoogleTranslate, using translators")
            return ts.translate_html(html, to_language=to_lang, from_language=from_lang)
        except Exception as e:
            self.logger.error(f"HTML translation failed: {e}")
            return None