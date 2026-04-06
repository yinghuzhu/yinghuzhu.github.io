# EspoCRM 定制开发：升级安全与工程化规范

## 适用版本

EspoCRM 9.2.2+（开源版）

---

## 背景

很多团队做 EspoCRM 定制，第一阶段靠"改得快"赢；第二阶段会被"不可升级、不可回滚、不可定位问题"拖垮。

具体表现：

- 花两周做的定制，官方更新后全部失效
- 团队成员改了核心文件，导致无法升级
- 代码和配置混在一起，出问题无法定位
- 没有备份机制，系统崩溃后无法恢复

本文的目标很明确：**不讨论"改核心文件最快"的玩法，只讨论"升级后仍可活"的做法**。

---

## 阅读指引

### 适合谁读

```
□ 第一次用 EspoCRM 做定制开发
□ 升级时曾经踩过坑
□ 需要给团队定开发规范
□ 正在做企业级项目，不能冒险
```

### 读完你能获得

1. 一套可复制的 EspoCRM 定制开发模板
2. 扩展点选择优先级（金字塔）
3. 完整的模块结构与部署规范
4. 可直接使用的备份与回滚脚本

---

## 一、扩展点选择金字塔

### 1.1 默认策略：能不写代码就不写代码

| 优先级 | 扩展点 | 适用场景 |
|:-------|:-------|:---------|
| 1 | Formula | 简单计算和条件逻辑 |
| 2 | Dynamic Logic | 界面显示与字段依赖 |
| 3 | Workflow / BPM | 复杂业务流程（谨慎用） |
| 4 | Hook | 数据一致性保障（禁止重逻辑） |
| 5 | Service / Controller | API 与复杂逻辑（最后手段） |

**核心原则**：先用 Dynamic Logic 解决体验问题，再用 Hook/Service 解决"绕过与一致性"。

### 1.2 五条红线

| 红线 | 后果 |
|:-----|:-----|
| 不修改 `application/` 目录 | 每次升级都要重写 |
| 不硬编码环境信息 | 迁移环境就爆炸 |
| 不混用配置与代码 | 无法审计、无法回滚 |
| Hook 里不做重逻辑 | 会阻塞保存流程 |
| 不绕过 ACL | 安全事故 |

---

## 二、模块化架构

### 2.1 目录分区原则

**核心思想**：把管理员（GUI）产生的配置，和开发者（代码）交付的内容，物理隔离。

```
custom/
├── Espo/Custom/                    # 管理员配置区
│   └── Resources/metadata/
└── Espo/Modules/{ModuleName}/      # 开发者模块区
    ├── Controllers/
    ├── Services/
    ├── Hooks/
    └── Resources/
        ├── metadata/
        └── i18n/
```

为什么？因为管理员配置可变、不可审计，而开发者代码必须可审计、可回滚、可复现。

### 2.2 完整后端模块结构

```
custom/Espo/Modules/MyModule/
├── Module.php                          # 模块定义类
├── Controllers/                        # API 控制器
├── Services/                           # 业务逻辑服务层
├── Hooks/                              # 数据钩子
│   ├── MyEntity/BeforeSave.php
│   └── AnotherEntity/AfterSave.php
├── Jobs/                               # 定时任务
├── Entities/                           # 实体类（可选）
└── Resources/                          # 元数据与配置
    ├── metadata/
    │   ├── entityDefs/                 # 实体定义
    │   ├── clientDefs/                 # 前端定义
    │   ├── scopes/                     # 权限作用域
    │   └── routes.json                 # API 路由
    ├── layouts/                        # 界面布局
    └── i18n/                           # 语言包
```

### 2.3 前端模块结构

```
client/modules/my-module/
└── src/
    ├── views/                           # 自定义视图
    ├── fields/                          # 自定义字段类型
    └── templates/                       # 模板
```

---

## 三、各层职责分工

### 3.1 Controller：API 入口

**职责**：处理 HTTP 请求 → 权限检查 → 调用 Service → 返回 JSON

```php
<?php
namespace Espo\Modules\MyModule\Controllers;

use Espo\Core\Controllers\Record;
use Espo\Core\Exceptions\BadRequest;
use Espo\Core\Exceptions\Forbidden;

class MyEntity extends Record
{
    public function actionMyAction($params, $data, $request)
    {
        // 1. 权限检查
        if (!$this->getUser()->isAdmin()) {
            throw new Forbidden();
        }

        // 2. 参数验证
        if (empty($data->param)) {
            throw new BadRequest("param is required");
        }

        // 3. 调用 Service
        return $this->getContainer()
            ->get('MyService')
            ->doSomething($data->param);
    }
}
```

### 3.2 Service：业务逻辑层

**职责**：复杂业务逻辑、跨实体操作、调用外部 API

```php
<?php
namespace Espo\Modules\MyModule\Services;

use Espo\Core\ORM\EntityManager;
use Espo\Core\Utils\Config;
use Espo\Core\Utils\Log;

class MyService
{
    public function __construct(
        private EntityManager $entityManager,
        private Config $config,
        private Log $log
    ) {}

    public function doSomething(string $param): array
    {
        $this->log->info("MyService::doSomething started");

        // 业务逻辑
        $result = $this->processData($param);

        $this->log->info("MyService::doSomething completed");

        return $result;
    }

    private function processData(string $param): array
    {
        // ...
    }
}
```

### 3.3 Hook：数据一致性保障

**职责**：保存前校验/补充、保存后联动、删除前检查

**红线**：不发邮件、不做 HTTP 请求、不做复杂计算

```php
<?php
namespace Espo\Modules\MyModule\Hooks\MyEntity;

use Espo\ORM\Entity;
use Espo\Core\Exceptions\BadRequest;

class BeforeSave
{
    public function beforeSave(Entity $entity, array $options): void
    {
        // 校验
        if ($entity->get('status') === 'Closed'
            && !$entity->get('closedReason')
        ) {
            throw new BadRequest("closedReason is required");
        }

        // 数据补充
        if ($entity->isNew()) {
            $entity->set('assignedUserId', $this->getUser()->id);
        }
    }
}
```

### 3.4 Job：定时后台任务

**职责**：定时触发、批量数据处理、发送通知/邮件

```php
<?php
namespace Espo\Modules\MyModule\Jobs;

use Espo\Core\Job\JobDataLess;
use Espo\Core\ORM\EntityManager;
use Espo\Core\Utils\Log;

class MyScheduledJob implements JobDataLess
{
    public function __construct(
        private EntityManager $entityManager,
        private Log $log
    ) {}

    public function run(): void
    {
        $this->log->info('MyScheduledJob started');

        // 定时任务逻辑

        $this->log->info('MyScheduledJob completed');
    }
}
```

---

## 四、rebuild 与 clear-cache

### 4.1 操作清单

| 操作 | 必须 |
|:-----|:-----|
| 改 metadata（entityDefs / clientDefs / scopes / routes） | rebuild |
| 改前端视图或模板 | clear-cache + 浏览器强刷 |
| 改语言包 | rebuild |

### 4.2 执行方式

```bash
CONTAINER_NAME="<your-espocrm-container>"
docker exec "$CONTAINER_NAME" php /var/www/html/command.php rebuild
docker exec "$CONTAINER_NAME" php /var/www/html/command.php clear-cache
```

---

## 五、总结

### 5.1 工程模板

每个需求按同一模板交付：

```
├── 需求与验收标准
├── 扩展点选择与理由
├── 技术设计与数据流
├── 代码实现（模块边界内）
├── 测试（UI + API + 边界）
├── 部署脚本（逐文件拷贝）
└── 回滚策略
```

### 5.2 核心原则

1. **能配置就不写代码** —— 用好 Formula、Dynamic Logic
2. **能扩展就不重写** —— 默认看板能扩展就别完全重写
3. **改动锁在模块内** —— 不改 `application/` 目录
4. **rebuild 是纪律** —— 改元数据必须 rebuild

---

