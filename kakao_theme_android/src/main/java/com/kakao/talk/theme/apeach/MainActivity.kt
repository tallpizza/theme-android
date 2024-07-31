package com.kakao.talk.theme.apeach

import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.WindowInsetsController
import android.view.WindowManager
import com.kakao.talk.theme.apeach.databinding.MainActivityBinding

open class MainActivity : Activity() {

    private lateinit var binding: MainActivityBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = MainActivityBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSystemStatusBar()

        binding.apply.setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW)
            intent.data = Uri.parse(KAKAOTALK_SETTINGS_THEME_URI + packageName)
            startActivity(intent)
            finish()
        }

        binding.market.setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(MARKET_URI + KAKAOTALK_PACKAGE_NAME))
            startActivity(intent)
            finish()
        }

        if (isKakaoTalkInstalled()) {
            binding.apply.visibility = View.VISIBLE
            binding.market.visibility = View.GONE
        } else {
            binding.apply.visibility = View.GONE
            binding.market.visibility = View.VISIBLE
        }
    }

    private fun setSystemStatusBar() = kotlin.runCatching {
        window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.statusBarColor = resources.getColor(R.color.statusBarColor, null)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            window.insetsController?.setSystemBarsAppearance(
                WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS,
                WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
            )
        } else {
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
        }
    }



    open fun isKakaoTalkInstalled(): Boolean {
        return try {
            packageManager.getPackageInfo(KAKAOTALK_PACKAGE_NAME, 0)
            true
        } catch (e: PackageManager.NameNotFoundException) {
            false
        }
    }

    companion object {
        private const val KAKAOTALK_SETTINGS_THEME_URI = "kakaotalk://settings/theme/"
        private const val MARKET_URI = "market://details?id="
        const val KAKAOTALK_PACKAGE_NAME = "com.kakao.talk"
    }
}
