import { t } from "ttag";
import RequestUtils from "services/helpers/request_utils";

const urlMap = {
    base: {
        prefix: "account/role",
        endpoints: {
            crud: ""
        }
    }
};
export const urls = RequestUtils.prefixMapValues(urlMap.base);

const headingTxt = t`Group`;
const name = headingTxt.toLowerCase();
export const messages = {
    heading: headingTxt,
    deleteOne: t`Do you want to remote this ${name}?`,
    deleteMultiple: t`Do you want to remote these ${name}?`
};

export const emptyRecord = {
    id: 0,
    name: "",
    permissions: []
};

export const labels = {
    name: t`Group name`,
    permissions: t`Permissions`
};

export const excludeGroups = ["user", "logentry", "token", "contenttype", "session"];
