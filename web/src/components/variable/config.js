import { t } from "ttag";
import RequestUtils from "services/helpers/request_utils";

const urlMap = {
    base: {
        prefix: "configuration/variable",
        endpoints: {
            crud: ""
        }
    }
};
export const urls = RequestUtils.prefixMapValues(urlMap.base);

const headingTxt = t`Config`;
const name = headingTxt.toLowerCase();
export const messages = {
    heading: headingTxt,
    deleteOne: t`Do you want to remote this ${name}?`,
    deleteMultiple: t`Do you want to remote these ${name}?`
};

export const labels = {
    uid: t`Config name`,
    value: t`Config value`
};
