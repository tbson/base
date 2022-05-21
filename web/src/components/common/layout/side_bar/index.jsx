import * as React from "react";
import { useState } from "react";
import { useNavigate, useLocation, NavLink, Outlet } from "react-router-dom";
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
import NavUtils from "services/helpers/nav_utils";
import LocaleSelect from "components/common/locale_select.jsx";
import styles from "./styles.module.css";

const { SubMenu } = Menu;

const { Header, Sider, Content } = Layout;

/**
 * SideBarLayout.
 */
export default function SideBarLayout() {
    const navigate = useNavigate();
    const location = useLocation();

    const [collapsed, setCollapsed] = useState(false);
    const toggle = () => {
        setCollapsed(!collapsed);
    };

    const visibleMenus = StorageUtils.getVisibleMenus();
    const logout = NavUtils.logout(navigate);

    /**
     * processSelectedKey.
     *
     * @param {string} pathname
     * @returns {string}
     */
    const processSelectedKey = (pathname) => {
        if (pathname.startsWith("/staff")) return "/staff";
        return pathname;
    };

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
                    selectedKeys={[processSelectedKey(location.pathname)]}
                    theme="dark"
                    mode="inline"
                    defaultOpenKeys={["company"]}
                >
                    <Menu.Item key="/">
                        <NavLink to="/">
                            <UserOutlined />
                            <MenuLabel collapsed={collapsed} label="Hồ sơ" />
                        </NavLink>
                    </Menu.Item>

                    {visibleMenus.includes("variable") && (
                        <Menu.Item key="/variable">
                            <NavLink to="/variable">
                                <SettingFilled />
                                <MenuLabel collapsed={collapsed} label="Cấu hình" />
                            </NavLink>
                        </Menu.Item>
                    )}
                    <SubMenu key="company" icon={<GoldenFilled />} title="Công ty">
                        {visibleMenus.includes("staff") && (
                            <Menu.Item key="/staff">
                                <NavLink to="/staff">
                                    <TeamOutlined />
                                    <MenuLabel
                                        collapsed={collapsed}
                                        label="Nhân viên"
                                    />
                                </NavLink>
                            </Menu.Item>
                        )}
                        {visibleMenus.includes("group") && (
                            <Menu.Item key="/role">
                                <NavLink to="/role">
                                    <UsergroupAddOutlined />
                                    <MenuLabel collapsed={collapsed} label="Nhóm" />
                                </NavLink>
                            </Menu.Item>
                        )}
                    </SubMenu>
                </Menu>
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
            </Layout>
        </Layout>
    );
}

/**
 * MenuLabel.
 *
 * @param {Object} props
 * @param {boolean} props.collapsed
 * @param {string} props.label
 * @returns {ReactElement}
 */
function MenuLabel({ collapsed, label }) {
    if (collapsed) return null;
    return <span>&nbsp;{label}</span>;
}
