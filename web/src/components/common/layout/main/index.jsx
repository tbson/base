import * as React from "react";
import { useState } from "react";
import { useNavigate, useLocation, Outlet } from "react-router-dom";
import { t } from "ttag";
import { Layout, Menu, Row, Col } from "antd";
import {
    MenuUnfoldOutlined,
    MenuFoldOutlined,
    UserOutlined,
    TeamOutlined,
    LogoutOutlined,
    SettingFilled,
    UsergroupAddOutlined,
    GoldenFilled
} from "@ant-design/icons";
import { LOGO_TEXT } from "src/consts";
import StorageUtils from "services/helpers/storage_utils";
import PemUtils from "services/helpers/pem_utils";
import NavUtils from "services/helpers/nav_utils";
import LocaleSelect from "components/common/locale_select.jsx";
import styles from "./styles.module.css";

const { Header, Footer, Sider, Content } = Layout;

/**
 * MainLayout.
 */
export default function MainLayout() {
    const navigate = useNavigate();
    const location = useLocation();

    const [collapsed, setCollapsed] = useState(false);
    const toggle = () => {
        setCollapsed(!collapsed);
    };

    const logout = NavUtils.logout(navigate);
    const navigateTo = NavUtils.navigateTo(navigate);

    /**
     * processSelectedKey.
     *
     * @param {string} pathname
     * @returns {string}
     */
    function processSelectedKey(pathname) {
        if (pathname.startsWith("/staff")) return "/staff";
        return pathname;
    }

    function getMenuItems() {
        const result = [];

        result.push({ label: t`Profile`, key: "/", icon: <UserOutlined /> });

        PemUtils.canView("variable") &&
            result.push({
                label: t`Config`,
                key: "/variable",
                icon: <SettingFilled />
            });

        if (PemUtils.canView(["staff", "group"])) {
            const companyGroup = {
                label: t`Company`,
                icon: <GoldenFilled />,
                children: []
            };
            PemUtils.canView("staff") &&
                companyGroup.children.push({
                    label: t`Staff`,
                    key: "/staff",
                    icon: <TeamOutlined />
                });
            PemUtils.canView("group") &&
                companyGroup.children.push({
                    label: t`Group`,
                    key: "/role",
                    icon: <UsergroupAddOutlined />
                });
            result.push(companyGroup);
        }
        return result;
    }

    return (
        <Layout className={styles.wrapperContainer}>
            <Sider
                trigger={null}
                breakpoint="lg"
                collapsedWidth="80"
                collapsible
                collapsed={collapsed}
                onBreakpoint={(broken) => {
                    setCollapsed(broken);
                }}
            >
                <div className="logo">{collapsed || LOGO_TEXT}</div>
                <Menu
                    className="sidebar-nav"
                    defaultSelectedKeys={[processSelectedKey(location.pathname)]}
                    theme="dark"
                    mode="inline"
                    items={getMenuItems()}
                    onSelect={({ key }) => navigateTo(key)}
                />
            </Sider>
            <Layout className="site-layout">
                <Header className="site-layout-header" style={{ padding: 0 }}>
                    <Row>
                        <Col span={12}>
                            {React.createElement(
                                collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
                                {
                                    className: "trigger",
                                    onClick: toggle
                                }
                            )}
                        </Col>
                        <Col span={12} className="right" style={{ paddingRight: 20 }}>
                            <LocaleSelect />
                            <span
                                onClick={logout}
                                onKeyDown={() => {}}
                                onKeyUp={() => {}}
                                onKeyPress={() => {}}
                                className="pointer"
                                role="button"
                                tabIndex="0"
                            >
                                <span>
                                    {StorageUtils.getStorageObj("auth").fullname}
                                </span>
                                &nbsp;&nbsp;
                                <LogoutOutlined />
                            </span>
                        </Col>
                    </Row>
                </Header>
                <Content className="site-layout-content">
                    <Outlet />
                </Content>
                <Footer className="layout-footer">Copyright base.test 2022</Footer>
            </Layout>
        </Layout>
    );
}
