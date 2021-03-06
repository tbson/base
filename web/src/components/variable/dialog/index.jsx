import * as React from "react";
import { useState, useEffect } from "react";
import { t } from "ttag";
import { Modal } from "antd";
import Utils from "services/helpers/utils";
import RequestUtils from "services/helpers/request_utils";
import Form from "./form";
import { urls, messages } from "../config";

export class Service {
    static get toggleEvent() {
        return "TOGGLE_VARIABLE_DIALOG";
    }

    static toggle(open = true, id = 0) {
        Utils.event.dispatch(Service.toggleEvent, { open, id });
    }
}

/**
 * VariableDialog.
 *
 * @param {Object} props
 * @param {function} props.onChange - (data: Dict, id: number) => void
 */
export default function VariableDialog({ onChange }) {
    const [data, setData] = useState({});
    const [open, setOpen] = useState(false);
    const [id, setId] = useState(0);

    const handleToggle = ({ detail: { open, id } }) => {
        if (!open) return setOpen(false);
        setId(id);
        if (id) {
            Utils.toggleGlobalLoading();
            RequestUtils.apiCall(`${urls.crud}${id}`)
                .then((resp) => {
                    setData(resp.data);
                    setOpen(true);
                })
                .finally(() => Utils.toggleGlobalLoading(false));
        } else {
            setData({});
            setOpen(true);
        }
    };

    useEffect(() => {
        Utils.event.listen(Service.toggleEvent, handleToggle);
        return () => {
            Utils.event.remove(Service.toggleEvent, handleToggle);
        };
    }, []);

    return (
        <Modal
            keyboard={false}
            maskClosable={false}
            destroyOnClose
            visible={open}
            okButtonProps={{ form: Form.formName, key: "submit", htmlType: "submit" }}
            okText={t`Save`}
            onCancel={() => Service.toggle(false)}
            cancelText={t`Cancel`}
            title={Utils.getDialogTitle(id, messages)}
        >
            <Form
                data={data}
                onChange={(data, id) => {
                    setOpen(false);
                    onChange(data, id);
                }}
            />
        </Modal>
    );
}

VariableDialog.displayName = "VariableDialog";
VariableDialog.toggle = Service.toggle;
