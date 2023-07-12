import * as React from "react";
import { useRef, useEffect } from "react";
import { useRecoilValue } from "recoil";
import { Form, Input } from "antd";
import Util from "service/helper/util";
import FormUtil from "service/helper/form_util";
import SelectInput from "component/common/form/ant/input/select_input.jsx";
import CheckInput from "component/common/form/ant/input/check_input.jsx";
import { urls, labels, emptyRecord } from "../config";
import { staffOptionsSt } from "../states";

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
    const inputRef = useRef(null);
    const [form] = Form.useForm();
    const staffOptions = useRecoilValue(staffOptionsSt);

    const initialValues = Util.isEmpty(data) ? emptyRecord : { ...data };
    const id = initialValues.id;
    const endPoint = id ? `${urls.crud}${id}` : urls.crud;
    const method = id ? "put" : "post";

    const formAttrs = {
        email: {
            name: "email",
            label: labels.email,
            rules: [FormUtil.ruleRequired()]
        },
        phone_number: {
            name: "phone_number",
            label: labels.phone_number
        },
        last_name: {
            name: "last_name",
            label: labels.last_name,
            rules: [FormUtil.ruleRequired()]
        },
        first_name: {
            name: "first_name",
            label: labels.first_name,
            rules: [FormUtil.ruleRequired()]
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

    useEffect(() => {
        inputRef.current.focus({ cursor: "end" });
    }, []);

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 4 }}
            wrapperCol={{ span: 20 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtil.submit(endPoint, payload, method)
                    .then((data) => onChange(data, id))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.email}>
                <Input ref={inputRef}/>
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
                <SelectInput options={staffOptions.group} mode="multiple" block />
            </Form.Item>
            <Form.Item {...formAttrs.is_active}>
                <CheckInput />
            </Form.Item>
        </Form>
    );
}

StaffForm.displayName = formName;
StaffForm.formName = formName;
