package com.hellocmu.picoctf;

import android.content.Context;

/* loaded from: classes.dex */
public class FlagstaffHill {
    public static native String fenugreek(String str);

    public static String getFlag(String input, Context ctx) {
        String password = ctx.getString(R.string.password);
        return input.equals(password) ? fenugreek(input) : "NOPE";
    }
}