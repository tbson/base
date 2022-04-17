import { Select } from "antd";
import LocaleUtils from "services/helpers/locale_utils";

const { Option } = Select;

function handleChange(value) {
    LocaleUtils.setLocale(value);
    location.reload();
}

export default function LocaleSelect() {
    return (
        <Select defaultValue={LocaleUtils.getLocale()} onChange={handleChange}>
            {LocaleUtils.getSupportedLocales().map((locale) => (
                <Option key={locale} value={locale}>
                    {locale}
                </Option>
            ))}
        </Select>
    );
}

LocaleSelect.displayName = "LocaleSelect";
