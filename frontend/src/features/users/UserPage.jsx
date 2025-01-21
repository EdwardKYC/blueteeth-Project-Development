import React from "react";
import { useSelector } from "react-redux";
import { useTable } from "react-table";
import './UserPage.css';

const UserPage = () => {
  const users = useSelector((state) => state.users.byName);

  const hasUsers = Object.keys(users).length > 0;

  const data = React.useMemo(
    () =>
      Object.values(users).map((user) => ({
        userName: user.userName,
        book: user.book ? user.book.name : "No book found",
        device: user.device
          ? { id: user.device.id, color: user.device.color }
          : null,
      })),
    [users]
  );

  const columns = React.useMemo(
    () => [
      { Header: "User Name", accessor: "userName" },
      { Header: "Book", accessor: "book" },
      {
        Header: "Device",
        accessor: "device",
        Cell: ({ value }) =>
          value ? (
            <div
              className="device-badge"
              style={{
                borderColor: value.color,
                color: value.color,
              }}
            >
              {value.id}
            </div>
          ) : (
            "No device linked"
          ),
      },
    ],
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  return (
    <div className="user-page">
      {hasUsers ? (
        <>
          <h1>User Page</h1>
          <table {...getTableProps()} className="modern-table">
            <thead>
              {headerGroups.map((headerGroup) => {
                const { key, ...rest } = headerGroup.getHeaderGroupProps();
                return (
                  <tr key={key} {...rest}>
                    {headerGroup.headers.map((column) => {
                      const { key: columnKey, ...columnRest } = column.getHeaderProps();
                      return (
                        <th key={columnKey} {...columnRest}>
                          {column.render("Header")}
                        </th>
                      );
                    })}
                  </tr>
                );
              })}
            </thead>
            <tbody {...getTableBodyProps()}>
              {rows.map((row) => {
                prepareRow(row);
                const { key, ...rest } = row.getRowProps();
                return (
                  <tr key={key} {...rest}>
                    {row.cells.map((cell) => {
                      const { key: cellKey, ...cellRest } = cell.getCellProps();
                      return (
                        <td key={cellKey} {...cellRest}>
                          {cell.render("Cell")}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      ) : (
        <h1>No Users Available</h1>
      )}
    </div>
  );
};

export default UserPage;