import RequestUtils from "services/helpers/request_utils";

const urlMap = {
    base: {
        prefix: "account/user",
        endpoints: {
            login: "login",
            signupConfirm: "signup-confirm",
            resetPassword: "reset-password",
            changePassword: "change-password"
        }
    },
    staff: {
        prefix: "account/staff",
        endpoints: {
            profile: "profile"
        }
    },
    verif: {
        prefix: "noti/verif",
        endpoints: {
            check: "check",
            resend: "resend"
        }
    }
};

export const urls = RequestUtils.prefixMapValues(urlMap.base);
export const verifUrls = RequestUtils.prefixMapValues(urlMap.verif);

const headingTxt = "Hồ sơ";
export const messages = {
    heading: headingTxt
};
