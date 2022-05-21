import { atom } from "recoil";
import LocaleUtils from "services/helpers/locale_utils";

export const localeSt = atom({
    key: "locale",
    default: LocaleUtils.getLocale()
});
