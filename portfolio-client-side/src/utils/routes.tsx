import React, { useMemo } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import type { IRoute } from "../types/router";

type IProps = {
  routes: IRoute[];
  routerPrefix?: string;
};

const GenerateRoutes = ({ routes, routerPrefix = "r" }: IProps) => {
  // group routes by outletKey
  const groupedRoutes = useMemo(() => {
    return routes.reduce<Record<string, IRoute[]>>((acc, curr) => {
      const key = curr.outletKey ?? "default";
      (acc[key] ||= []).push(curr);
      return acc;
    }, {});
  }, [routes]);

  return (
    <Routes>
      {Object.entries(groupedRoutes).map(([groupKey, groupRoutes]) => {
        const first = groupRoutes[0];
        const layoutEl = first?.outlet ?? undefined; // should be a JSX element like <AppLayout />

        return (
          <Route
            key={`${routerPrefix}-group-${groupKey}`}
            // if layoutEl is undefined, no layout wrapper; children will be rendered at root
            {...(layoutEl ? { element: layoutEl } : {})}
          >
            {groupRoutes.map((rt, idx) => {
              // Normalize path and index:
              // treat "/" or "" as index route
              const raw = rt.path ?? "";
              const normalized = raw.replace(/^\//, ""); // remove leading slash for relative path
              const isIndex = rt.index || raw === "/" || normalized === "";

              if (isIndex) {
                return (
                  <Route
                    key={`${routerPrefix}-${groupKey}-idx-${idx}`}
                    index
                    element={rt.element}
                  />
                );
              }

              return (
                <Route
                  key={`${routerPrefix}-${groupKey}-${idx}`}
                  path={normalized}
                  element={rt.element}
                />
              );
            })}
          </Route>
        );
      })}

      {/* optional catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default GenerateRoutes;