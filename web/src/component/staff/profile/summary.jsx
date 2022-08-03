import * as React from "react";
import { Row, Col } from "antd";
import { t } from "ttag";

export default function ProfileSummary(data) {
    return (
        <div>
            <Row>
                <Col span={6}>
                    <strong>{t`Email`}</strong>
                </Col>
                <Col span={18}>{data.email}</Col>
            </Row>
            <Row>
                <Col span={6}>
                    <strong>{t`Phone number`}</strong>
                </Col>
                <Col span={18}>{data.phone_number}</Col>
            </Row>
            <Row>
                <Col span={6}>
                    <strong>{t`Fullname`}</strong>
                </Col>
                <Col span={18}>{data.full_name}</Col>
            </Row>
        </div>
    );
}
ProfileSummary.displayName = "ProfileSummary";
