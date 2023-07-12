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
import StorageUtil from "service/helper/storage_util";
import PemUtil from "service/helper/pem_util";
import NavUtil from "service/helper/nav_util";
import LocaleSelect from "component/common/locale_select.jsx";
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

    const logout = NavUtil.logout(navigate);
    const navigateTo = NavUtil.navigateTo(navigate);

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

        PemUtil.canView("variable") &&
            result.push({
                label: t`Config`,
                key: "/variable",
                icon: <SettingFilled />
            });

        if (PemUtil.canView(["staff", "group"])) {
            const companyGroup = {
                label: t`Company`,
                icon: <GoldenFilled />,
                children: []
            };
            PemUtil.canView("staff") &&
                companyGroup.children.push({
                    label: t`Staff`,
                    key: "/staff",
                    icon: <TeamOutlined />
                });
            PemUtil.canView("group") &&
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
                <div className="sider">
                    <div className="logo">
                        <div className="logo-text">{collapsed || LOGO_TEXT}</div>
                    </div>
                    <Menu
                        className="sidebar-nav"
                        defaultSelectedKeys={[processSelectedKey(location.pathname)]}
                        theme="dark"
                        mode="inline"
                        items={getMenuItems()}
                        onSelect={({ key }) => navigateTo(key)}
                    />
                </div>
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
                                    {StorageUtil.getStorageObj("auth").fullname}
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
                <Footer className="layout-footer">
                    <div className="layout-footer-text">
                        Copyright basecode.test 2023
                    </div>
                </Footer>
            </Layout>
        </Layout>
    );
}
