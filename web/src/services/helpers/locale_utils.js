import { addLocale } from "ttag";
import StorageUtils from "services/helpers/storage_utils";

const DEFAULT_LOCALE = "vi";
const SUPPORTED_LOCALES = ["vi", "en"];

export default class LocaleUtils {
    static async fetchLocales() {
        const result = [];
        for (const locale of SUPPORTED_LOCALES) {
            const module = await import(`../../locale/${locale}.po.json`);
            const localeObj = module.default;
            addLocale(locale, localeObj);
            result.push(localeObj);
        }
        return result;
    }
    static setLocale(locale = DEFAULT_LOCALE) {
        StorageUtils.setStorage("locale", locale);
        // useLocale(locale);
        return locale;
    }
    static getLocale() {
        let locale = StorageUtils.getStorageStr("locale");
        return SUPPORTED_LOCALES.includes(locale) ? locale : DEFAULT_LOCALE;
    }
    static getSupportedLocales() {
        return SUPPORTED_LOCALES;
    }
}
