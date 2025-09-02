#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xc8d01d53, "module_layout" },
	{ 0xae2ae519, "param_ops_int" },
	{ 0xabac4112, "cdev_add" },
	{ 0x51b1c11d, "cdev_init" },
	{ 0xaf88e69b, "kmem_cache_alloc_trace" },
	{ 0xde310d05, "kmalloc_caches" },
	{ 0xcefb0c9f, "__mutex_init" },
	{ 0xbd462b55, "__kfifo_init" },
	{ 0xeb233a45, "__kmalloc" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0x30a80826, "__kfifo_from_user" },
	{ 0x3eeb2322, "__wake_up" },
	{ 0x3213f038, "mutex_unlock" },
	{ 0x4578f528, "__kfifo_to_user" },
	{ 0x89940875, "mutex_lock_interruptible" },
	{ 0x92540fbf, "finish_wait" },
	{ 0x8ddd8aad, "schedule_timeout" },
	{ 0x8c26d495, "prepare_to_wait_event" },
	{ 0xfe487975, "init_wait_entry" },
	{ 0x800473f, "__cond_resched" },
	{ 0xd9a5ea54, "__init_waitqueue_head" },
	{ 0xd0da656b, "__stack_chk_fail" },
	{ 0x92997ed8, "_printk" },
	{ 0x281823c5, "__kfifo_out_peek" },
	{ 0x6091b333, "unregister_chrdev_region" },
	{ 0x37a0cba, "kfree" },
	{ 0x37ce6741, "cdev_del" },
	{ 0x65487097, "__x86_indirect_thunk_rax" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0xbdfb6dbb, "__fentry__" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "F3EB8C3FBFD71B1ED8D9E3D");
