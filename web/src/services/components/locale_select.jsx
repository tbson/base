import { Select } from "antd";
import { useRecoilState } from "recoil";
import { useLocale } from "ttag";
import LocaleUtils from "services/helpers/locale_utils";
import { localeSt } from "src/states";

const { Option } = Select;

export default function LocaleSelect() {
    const [locale, setLocale] = useRecoilState(localeSt);
    useLocale(locale);
    return (
        <Select
            defaultValue={LocaleUtils.getLocale()}
            onChange={(value) => {
                setLocale(LocaleUtils.setLocale(value));
            }}
        >
            {LocaleUtils.getSupportedLocales().map((locale) => (
                <Option key={locale} value={locale}>
                    {locale}
                </Option>
            ))}
        </Select>
    );
}

LocaleSelect.displayName = "LocaleSelect";
