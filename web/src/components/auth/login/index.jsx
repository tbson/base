import * as React from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { t } from "ttag";
import { Row, Col, Card, Button } from "antd";
import NavUtils from "services/helpers/nav_utils";
import StorageUtils from "services/helpers/storage_utils";
import LocaleSelect from "components/common/locale_select.jsx";
import Form from "./form";
import OTPDialog from "../otp_dialog";
import ResetPwdDialog from "../reset_pwd";
import ResetPwdConfirmDialog from "../reset_pwd_confirm";

const styles = {
    wrapper: {
        marginTop: 20
    }
};
export default function Login() {
    const navigate = useNavigate();
    const navigateTo = NavUtils.navigateTo(navigate);

    useEffect(() => {
        StorageUtils.getToken() && navigateTo();
    }, []);

    function handleLogin(data) {
        const nextUrl = window.location.href.split("next=")[1] || "/";
        StorageUtils.setStorage("auth", data);
        navigateTo(nextUrl);
    }

    function onResetPassword() {
        OTPDialog.toggle(true);
    }

    function onOTP() {
        ResetPwdConfirmDialog.toggle();
    }

    return (
        <div>
            <div className="right content">
                <LocaleSelect />
            </div>
            <Row>
                <Col
                    xs={{ span: 24 }}
                    md={{ span: 12, offset: 6 }}
                    lg={{ span: 8, offset: 8 }}
                >
                    <Card title="Đăng nhập" style={styles.wrapper}>
                        <Form onChange={handleLogin}>
                            <>
                                <Button
                                    type="link"
                                    onClick={() => ResetPwdDialog.toggle()}
                                >
                                    {t`Forgot password`}
                                </Button>
                            </>
                        </Form>
                    </Card>
                </Col>
            </Row>
            <ResetPwdDialog onChange={onResetPassword} />
            <OTPDialog onChange={onOTP} />
            <ResetPwdConfirmDialog />
        </div>
    );
}
