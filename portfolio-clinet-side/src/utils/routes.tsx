import { Route, Routes } from "react-router-dom";
import type { IRoute } from "../types/router";
import { useMemo } from "react";

const generateRoutes = (routes: IRoute[], routerPrefix: string) => {

    const groupedRoutes = useMemo(() => {
        const groupedRoutes = routes.reduce((acc, curr) => {
            const key = curr.outletKey || "default"
            if(!acc[key]) acc[key] = [];
            acc[key].push(curr);
            return acc;
        }, {} as Record<string, IRoute[]>)
        return groupedRoutes;
    }, [routes])

    return (
    <Routes>
      {Object.entries(groupedRoutes).map(([groupKey, groupRoutes]) => {
        // pick the shared header/footer/outlet from the first route in the group (convention)
        const outlet = groupRoutes[0].outlet;


        // Parent route provides the layout; no `path` so it acts as a layout wrapper for its children.
        return (
          <Route
            key={`${routerPrefix}-group-${groupKey}`}
            element={
              outlet
            }
          >
            {groupRoutes.map((route, idx) => {
              // make child route path relative (remove leading slash if present)
              const childPath = route.path.replace(/^\//, "");
              return (
                <Route
                  key={`${routerPrefix}-${groupKey}-${idx}`}
                  path={childPath}
                  element={route.element}
                />
              );
            })}
          </Route>
        );
      })}

      {/* optional: fallback / catch-all can be added here */}
    </Routes>
  );
}

export default generateRoutes;