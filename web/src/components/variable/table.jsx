import * as React from "react";
import { useEffect, useState } from "react";
import { Row, Col, Table } from "antd";
import Pagination, { defaultLinks } from "components/common/table/pagination";
import SearchInput from "components/common/table/search_input";
import {
    AddNewBtn,
    RemoveSelectedBtn,
    EditBtn,
    RemoveBtn
} from "components/common/table/buttons";
import PemCheck from "components/common/pem_check";
import Utils from "services/helpers/utils";
import RequestUtils from "services/helpers/request_utils";
import Dialog from "./dialog";
import { urls, labels, messages } from "./config";

const PEM_GROUP = "variable";

export default function VariableTable() {
    const [init, setInit] = useState(true);
    const [list, setList] = useState([]);
    const [ids, setIds] = useState([]);
    const [links, setLinks] = useState(defaultLinks);

    const getList =
        (showLoading = true) =>
        (url = "", params = {}) => {
            showLoading && Utils.toggleGlobalLoading();
            RequestUtils.apiCall(url ? url : urls.crud, params)
                .then((resp) => {
                    setLinks(resp.data.links);
                    setList(Utils.appendKey(resp.data.items));
                })
                .finally(() => {
                    setInit(false);
                    showLoading && Utils.toggleGlobalLoading(false);
                });
        };

    function searchList(keyword) {
        getList()("", keyword ? { search: keyword } : {});
    }

    useEffect(() => {
        getList(false)();
    }, []);

    function onDelete(id) {
        const r = window.confirm(messages.deleteOne);
        if (!r) return;

        Utils.toggleGlobalLoading(true);
        RequestUtils.apiCall(`${urls.crud}${id}`, {}, "delete")
            .then(() => {
                setList([...list.filter((item) => item.id !== id)]);
            })
            .finally(() => Utils.toggleGlobalLoading(false));
    }

    function onBulkDelete(ids) {
        const r = window.confirm(messages.deleteMultiple);
        if (!r) return;

        Utils.toggleGlobalLoading(true);
        RequestUtils.apiCall(`${urls.crud}?ids=${ids.join(",")}`, {}, "delete")
            .then(() => {
                setList([...list.filter((item) => !ids.includes(item.id))]);
            })
            .finally(() => Utils.toggleGlobalLoading(false));
    }

    function onChange(data, id) {
        if (!id) {
            setList([{ ...data, key: data.id }, ...list]);
        } else {
            const index = list.findIndex((item) => item.id === id);
            data.key = data.id;
            list[index] = data;
            setList([...list]);
        }
    }

    const columns = [
        {
            key: "uid",
            title: labels.uid,
            dataIndex: "uid"
        },
        {
            key: "value",
            title: labels.value,
            dataIndex: "value",
            width: 150
        },
        {
            key: "action",
            title: "",
            fixed: "right",
            width: 90,
            render: (_text, record) => (
                <div className="flex-space">
                    <PemCheck pem_group={PEM_GROUP} pem="change">
                        <EditBtn onClick={() => Dialog.toggle(true, record.id)} />
                    </PemCheck>
                    <PemCheck pem_group={PEM_GROUP} pem="delete">
                        <RemoveBtn onClick={() => onDelete(record.id)} />
                    </PemCheck>
                </div>
            )
        }
    ];

    const rowSelection = {
        onChange: (ids) => {
            setIds(ids);
        }
    };

    return (
        <div>
            <Row>
                <Col span={12}>
                    <PemCheck pem_group={PEM_GROUP} pem="delete">
                        <RemoveSelectedBtn ids={ids} onClick={onBulkDelete} />
                    </PemCheck>
                </Col>
                <Col span={12} className="right">
                    <PemCheck pem_group={PEM_GROUP} pem="add">
                        <AddNewBtn onClick={() => Dialog.toggle()} />
                    </PemCheck>
                </Col>
            </Row>

            <SearchInput onChange={searchList} />

            <Table
                rowSelection={{
                    type: "checkbox",
                    ...rowSelection
                }}
                columns={columns}
                dataSource={list}
                loading={init}
                scroll={{ x: 1000 }}
                pagination={false}
            />
            <Pagination next={links.next} prev={links.previous} onChange={getList()} />
            <Dialog onChange={onChange} />
        </div>
    );
}

VariableTable.displayName = "VariableTable";
