使用步骤：

1. 在你的AndroidManifest.xml中增加一个meta节点：

		<application>
		  <meta-data
	            android:name="Channel"
	            android:value="你的渠道号" />
	    </application>

2. 在你需要渠道号的地方进行获取：

		ApplicationInfo appInfo = this.getPackageManager().getApplicationInfo(getPackageName(), PackageManager.GET_META_DATA);
        String channel = appInfo.metaData.getString("Channel");

3. 将你的release包放在目录script中

4. 在config文件夹中的channel.txt配置你的渠道列表，不能纯数字的渠道号

		xiaomi
		vivo
		...
	
5. 在config文件夹中的config.txt文件中配置你的签名配置

		别名
		签名密码
		别名密码
6. 把你的签名文件放到keystore文件夹下

7. 把你的release包放到script目录下

8. 最重要的一步：双击 >>> **多渠道打包.bat**