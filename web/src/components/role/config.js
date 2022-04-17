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

const headingTxt = "Nhóm";
export const messages = {
    heading: headingTxt,
    deleteOne: `Bạn có muốn xoá ${headingTxt.toLowerCase()} này?`,
    deleteMultiple: `Bạn có muốn xoá những ${headingTxt.toLowerCase()} này?`
};

export const emptyRecord = {
    id: 0,
    name: "",
    permissions: []
};

export const labels = {
    name: "Tên nhóm",
    permissions: "Quyền"
};

export const pemGroupTrans = {
    group: "Nhóm",
    permission: "Quyền",
    staff: "Nhân viên",
    variable: "Cấu hình"
};

export const excludeGroups = ["user", "logentry", "token", "contenttype", "session"];
