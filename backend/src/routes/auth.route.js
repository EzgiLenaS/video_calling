import express from "express";
import {signup, login, logout} from "../controllers/auth.controller.js";
import { protectRoute } from "../middleware/auth.middleware.js";

const authRoutes = express.Router();

authRoutes.post("/signup", signup);
authRoutes.post("/login", login);
authRoutes.post("/logout", logout);

// Check if user is logged in
authRoutes.get("/me", protectRoute, (req, res) => {
    res.status(200).json({ success: true, userWhichUsedInAppAndAuthRoute: req.user });
});

export default authRoutes;