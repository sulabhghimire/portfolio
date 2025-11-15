import { Outlet } from "react-router-dom";
import DefaultHeader from "../DefaultHeader";
import DefaultFooter from "../DefaultFooter";
import { motion } from "framer-motion";


type ComponentOrNull = React.FC<any> | null;

interface IAppLayoutProps{
    Header?: ComponentOrNull;
    Footer?: ComponentOrNull;
}

const AppLayout = ( {Header, Footer}: IAppLayoutProps) => {

    const HeaderComponent = Header || DefaultHeader;
    const FooterComponent = Footer || DefaultFooter;

    return (
            <div className="flex flex-col h-screen bg-white dark:bg-zinc-950">
                <div className="sticky top-0 z-40">
                    <HeaderComponent />
                </div>
                <main className="flex-1 overflow-auto">
                    <div className="max-w-6xl mx-auto px-4 py-8">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                            <div className="max-w-3xl mx-auto">
                                <motion.div
                                    initial={{ opacity: 0, y: 8 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.35 }}
                                >
                                    <Outlet />
                                </motion.div>
                            </div>
                        </div>
                    </div>
                </main>
                <FooterComponent/>
            </div>
    )


}

export default AppLayout;