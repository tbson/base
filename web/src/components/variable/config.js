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

const headingTxt = "Cấu hình";
export const messages = {
    heading: headingTxt,
    deleteOne: `Bạn có muốn xoá ${headingTxt.toLowerCase()} này?`,
    deleteMultiple: `Bạn có muốn xoá những ${headingTxt.toLowerCase()} này?`
};

export const emptyRecord = {
    id: 0,
    uid: "",
    value: ""
};

export const labels = {
    uid: "Tên cấu hình",
    value: "Giá trị"
};
