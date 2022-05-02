import RequestUtils from "services/helpers/request_utils";

const urlMap = {
    base: {
        prefix: "account/staff",
        endpoints: {
            crud: "",
            profile: "profile"
        }
    }
};
export const urls = RequestUtils.prefixMapValues(urlMap.base);

const headingTxt = "Nhân viên";
export const messages = {
    heading: headingTxt,
    deleteOne: `Bạn có muốn xoá ${headingTxt.toLowerCase()} này?`,
    deleteMultiple: `Bạn có muốn xoá những ${headingTxt.toLowerCase()} này?`
};

export const emptyRecord = {
    id: 0,
    last_name: "",
    first_name: "",
    email: "",
    phone_number: "",
    groups: []
};

export const labels = {
    full_name: "Họ và tên",
    email: "Email",
    phone_number: "Số điện thoại",
    is_active: "Kích hoạt",
    groups: "Nhóm"
};
