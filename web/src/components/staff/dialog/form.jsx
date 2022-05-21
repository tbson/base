import * as React from "react";
import { useRecoilValue } from "recoil";
import { Form, Input } from "antd";
import Utils from "services/helpers/utils";
import FormUtils from "services/helpers/form_utils";
import SelectInput from "components/common/form/ant/input/select_input.jsx";
import CheckInput from "components/common/form/ant/input/check_input.jsx";
import { urls, labels, emptyRecord } from "../config";
import { listGroupSt } from "../states";

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

const formName = "StaffForm";

/**
 * StaffForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */
export default function StaffForm({ data, onChange }) {
    const [form] = Form.useForm();
    const listGroup = useRecoilValue(listGroupSt);

    const initialValues = Utils.isEmpty(data) ? emptyRecord : { ...data };
    const id = initialValues.id;
    const endPoint = id ? `${urls.crud}${id}` : urls.crud;
    const method = id ? "put" : "post";

    const formAttrs = {
        email: {
            name: "email",
            label: labels.email,
            rules: [FormUtils.ruleRequired()]
        },
        phone_number: {
            name: "phone_number",
            label: labels.phone_number
        },
        last_name: {
            name: "last_name",
            label: labels.last_name,
            rules: [FormUtils.ruleRequired()]
        },
        first_name: {
            name: "first_name",
            label: labels.first_name,
            rules: [FormUtils.ruleRequired()]
        },
        groups: {
            name: "groups",
            label: labels.groups
        },
        is_active: {
            name: "is_active",
            label: labels.is_active
        }
    };

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 4 }}
            wrapperCol={{ span: 20 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtils.submit(endPoint, payload, method)
                    .then((data) => onChange(data, id))
                    .catch(FormUtils.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.email}>
                <Input />
            </Form.Item>
            <Form.Item {...formAttrs.phone_number}>
                <Input />
            </Form.Item>
            <Form.Item {...formAttrs.last_name}>
                <Input />
            </Form.Item>
            <Form.Item {...formAttrs.first_name}>
                <Input />
            </Form.Item>
            <Form.Item {...formAttrs.groups}>
                <SelectInput options={listGroup} mode="multiple" />
            </Form.Item>
            <Form.Item {...formAttrs.is_active}>
                <CheckInput />
            </Form.Item>
        </Form>
    );
}

StaffForm.displayName = formName;
StaffForm.formName = formName;
