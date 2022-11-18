from BP import user_bp


@user_bp.route('/profix')
def user_():
    return '蓝图导入成功!'
