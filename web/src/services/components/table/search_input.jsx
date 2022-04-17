import * as React from "react";
import { Input } from "antd";
const { Search } = Input;

/**
 * @callback onChange
 * @param {string} keyword
 */

/**
 * SearchInput.
 *
 * @param {Object} props
 * @param {boolean} props.show
 * @param {onChange} props.onChange
 * @returns {ReactElement}
 */
export default function SearchInput({ show = true, onChange }) {
    if (!show) return null;
    return (
        <div>
            <Search name="keyword" placeholder="Search..." onSearch={onChange} />
        </div>
    );
}
