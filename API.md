# One Piece API 接口文档

**Base URL:** `http://localhost:8080/api`

**统一响应格式:**
```json
{
  "success": true|false,
  "data": {},
  "message": "可选消息"
}
```

---

## 认证接口

### POST /auth/login

用户登录，获取 JWT Token。

**请求体:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "admin",
      "created_at": "2024-01-01T00:00:00"
    }
  },
  "message": "登录成功"
}
```

**失败响应:** `401 Unauthorized`
```json
{
  "success": false,
  "message": "用户名或密码错误"
}
```

---

### GET /auth/verify

验证 Token 有效性。

**请求头:**
```
Authorization: Bearer <token>
```

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "admin"
  }
}
```

**失败响应:** `401 Unauthorized`
```json
{
  "success": false,
  "message": "token已过期"
}
```

---

## 船员接口

### GET /crew/members

获取所有船员列表。

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "蒙奇·D·路飞",
      "role": "船长",
      "bounty": "30亿贝里",
      "image_url": "https://...",
      "description": "橡胶果实能力者...",
      "abilities": {
        "devil_fruit": "橡胶果实（尼卡形态）",
        "haki_types": "霸王色霸气、武装色霸气、见闻色霸气",
        "special_skills": "四档、五档变身",
        "signature_moves": "橡胶火箭炮、橡胶象枪..."
      },
      "pirate_group_id": 1,
      "pirate_group_name": "草帽海贼团",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

### GET /crew/members/:id

获取单个船员详情。

**路径参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 船员ID |

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "蒙奇·D·路飞",
    "role": "船长",
    "bounty": "30亿贝里",
    "image_url": "https://...",
    "description": "橡胶果实能力者...",
    "abilities": {
      "devil_fruit": "橡胶果实（尼卡形态）",
      "haki_types": "霸王色霸气、武装色霸气、见闻色霸气",
      "special_skills": "四档、五档变身",
      "signature_moves": "橡胶火箭炮、橡胶象枪..."
    },
    "pirate_group_id": 1,
    "pirate_group_name": "草帽海贼团",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**失败响应:** `404 Not Found`
```json
{
  "success": false,
  "message": "船员不存在"
}
```

---

## 海贼团接口

### GET /pirate-groups

获取所有海贼团列表（不含成员）。

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "草帽海贼团",
      "captain": "蒙奇·D·路飞",
      "ship_name": "千阳号",
      "total_bounty": "88.16亿贝里",
      "flag_description": "带草帽的骷髅旗",
      "origin": "东海",
      "member_count": 10,
      "description": "由蒙奇·D·路飞创建的海贼团...",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

### GET /pirate-groups/:id

获取海贼团详情（含成员列表）。

**路径参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 海贼团ID |

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "草帽海贼团",
    "captain": "蒙奇·D·路飞",
    "ship_name": "千阳号",
    "total_bounty": "88.16亿贝里",
    "flag_description": "带草帽的骷髅旗",
    "origin": "东海",
    "member_count": 10,
    "description": "由蒙奇·D·路飞创建的海贼团...",
    "created_at": "2024-01-01T00:00:00",
    "members": [
      {
        "id": 1,
        "name": "蒙奇·D·路飞",
        "role": "船长",
        "bounty": "30亿贝里",
        "..."
      }
    ]
  }
}
```

**失败响应:** `404 Not Found`
```json
{
  "success": false,
  "message": "海贼团不存在"
}
```

---

### GET /pirate-groups/:id/members

获取指定海贼团的成员列表。

**路径参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 海贼团ID |

**成功响应:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "蒙奇·D·路飞",
      "role": "船长",
      "bounty": "30亿贝里",
      "..."
    }
  ]
}
```

**失败响应:** `404 Not Found`
```json
{
  "success": false,
  "message": "海贼团不存在"
}
```

---

## 错误码说明

| HTTP状态码 | 说明 |
|-----------|------|
| 200 | 请求成功 |
| 401 | 未授权（登录失败/Token无效） |
| 404 | 资源不存在 |
| 405 | 请求方法不允许 |
| 500 | 服务器内部错误 |

---

## 测试账号

| 用户名 | 密码 |
|--------|------|
| admin | admin123 |
| user | user123 |
