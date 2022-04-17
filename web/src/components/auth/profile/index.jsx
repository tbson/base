import { useEffect, useState } from "react";
import { Divider, Button } from "antd";
import { KeyOutlined, UserOutlined } from "@ant-design/icons";
import Wrapper from "services/components/wrapper";
import PageHeading from "services/components/page_heading";
import RequestUtils from "services/helpers/request_utils";
import { urls, messages } from "../config";
import Sumarry from "./summary";
import UpdateProfile from "./update_profile";
import ChangePwd from "./change_pwd";

export const emptyProfile = {
    id: 0,
    email: "",
    phone_number: "",
    first_name: "",
    last_name: "",
    title_label: "",
    list_parent: []
};

export default function Profile() {
    const [profileData, setProfileData] = useState(emptyProfile);
    useEffect(() => {
        RequestUtils.apiCall(urls.profile).then((resp) => {
            setProfileData(resp.data);
        });
    }, []);
    return (
        <Wrapper>
            <>
                <PageHeading>
                    <>{messages.heading}</>
                </PageHeading>
                <div className="content">
                    <Sumarry {...profileData} />
                    <Divider />
                    <Button
                        htmlType="button"
                        type="primary"
                        icon={<UserOutlined />}
                        onClick={() => UpdateProfile.toggle(true, profileData)}
                    >
                        Cập nhật hồ sơ
                    </Button>
                    &nbsp;&nbsp;
                    <Button
                        htmlType="button"
                        icon={<KeyOutlined />}
                        onClick={() => ChangePwd.toggle()}
                    >
                        Đổi mật khẩu
                    </Button>
                    <UpdateProfile onChange={(data) => setProfileData(data)} />
                    <ChangePwd />
                </div>
            </>
        </Wrapper>
    );
}

Profile.displayName = "Profile";
