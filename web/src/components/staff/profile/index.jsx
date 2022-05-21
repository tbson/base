import * as React from "react";
import { useEffect, useState } from "react";
import { Divider, Button } from "antd";
import { KeyOutlined, UserOutlined } from "@ant-design/icons";
import SideBarLayout from "components/common/layout/side_bar";
import PageHeading from "components/common/page_heading";
import RequestUtils from "services/helpers/request_utils";
import ChangePwd from "components/auth/change_pwd";
import { urls, messages } from "../config";
import ProfileSummary from "./summary";
import UpdateProfile from "./update_profile";

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
        <SideBarLayout>
            <>
                <PageHeading>
                    <>{messages.heading}</>
                </PageHeading>
                <div className="content">
                    <ProfileSummary {...profileData} />
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
        </SideBarLayout>
    );
}

Profile.displayName = "Profile";
