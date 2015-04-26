from pyethereum import tester
from datetime import datetime, date

from utilRelay import makeMerkleProof

import pytest
slow = pytest.mark.slow

class TestBtcBulkStoreHeaders(object):

    CONTRACT = 'btcBulkStoreHeaders.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        # needed for 10 headers testing only since max is 3M
        tester.gas_limit = 5 * 10**6
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testTx1In300K(self):
        hh = self.bulkStore10From300K()

        txIndex = 1
        # block300k tx[1] 7301b595279ece985f0c415e420e425451fcf7f684fcce087ba14d10ffec1121
        txStr = '01000000014dff4050dcee16672e48d755c6dd25d324492b5ea306f85a3ab23b4df26e16e9000000008c493046022100cb6dc911ef0bae0ab0e6265a45f25e081fc7ea4975517c9f848f82bc2b80a909022100e30fb6bb4fb64f414c351ed3abaed7491b8f0b1b9bcd75286036df8bfabc3ea5014104b70574006425b61867d2cbb8de7c26095fbc00ba4041b061cf75b85699cb2b449c6758741f640adffa356406632610efb267cb1efa0442c207059dd7fd652eeaffffffff020049d971020000001976a91461cf5af7bb84348df3fd695672e53c7d5b3f3db988ac30601c0c060000001976a914fd4ed114ef85d350d6d40ed3f6dc23743f8f99c488ac00000000'
        btcAddr = 0x61cf5af7bb84348df3fd695672e53c7d5b3f3db9
        self.checkRelay(txStr, txIndex, btcAddr, hh)


    # this is a static test.  for a broader test,
    # there's a veryslow dynamic test that calls randomTxVerify in test_txVerify.py
    @slow
    def testRelay300K(self):
        hh = self.bulkStore10From300K()

        txIndex = 3
        txStr = '0100000002acf17f885a83c7a221ab64fda59bce530b95a131a16eff3470a6cccac6b2d312000000006b483045022100a71b9fe6d94918b436e7b949f6c49407f25e4e39fc7fe20cf22e787def43cb5602200b52e999c0e75eaef28bd97609465ff41d7dad99e06b219997c3df452251e903012102e7d08484e6c4c26bd2a3aabab09c65bbdcb4a6bba0ee5cf7008ef19b9540f818ffffffff71d4a7c7fe372cb80d7170b96a8a2b8c5a0b0015f7877f50e6709fc78f1766ae010000006b483045022100c82137d106505ab32febf6ba3a607fe62cd4a4ab96fef67bf4e379405c40836302202cf6d85f4a0e811728870d649ceb47b24986599f0f09c252e9b62c94df6a2bb5012102e7d08484e6c4c26bd2a3aabab09c65bbdcb4a6bba0ee5cf7008ef19b9540f818ffffffff0200743ba40b0000001976a91429a158767437cd82ccf4bd3e34ecd16c267fc36388ace093a7ca000000001976a9140b31340661bb7a4165736ca2fc6509164b1dc96488ac00000000'
        btcAddr = 0x29a158767437cd82ccf4bd3e34ecd16c267fc363
        self.checkRelay(txStr, txIndex, btcAddr, hh)

        txIndex = 9
        txStr = '0100000001afb74944e62f5182cfeac80d2039e263f84a41af698aa9d04dd8a23c452bba04010000006a473044022023ff1153282b9e7f6b6d2d5ead84f9a6ab8cf15c91955160c3e79c49cf06802102203f882a1d71c0eff3985e276c4bb01c4d5762632cba3ce43818c60d31b76d8a450121034809fb967e89f40e4509179af367658263e0236ed9251a3b9f85c995715f7c38ffffffff02fbe9cd32000000001976a9142677ecb4e52311a83a3239f5fbff8c5325f7ebc988ac055aebc9000000001976a9146c6c734aeca979d3e190762cabd70b26e05f105f88ac00000000'
        btcAddr = 0x2677ecb4e52311a83a3239f5fbff8c5325f7ebc9
        self.checkRelay(txStr, txIndex, btcAddr, hh)

        txIndex = 216
        txStr = '0100000008e8cd5987582c32393e41358baf37c1558de6ab061be42a497692cdea5784b1e9000000006b483045022100d44a3d698afde6df43f6a2387d6356716dde81e743676d8abe6efc0f7a196a56022036cc81b319a24605463a47a2f0605a9e1496a26e71990ef32301b118f53691ab0121033a6942b7436d179f1fa03434fc2b0f7e66841f826cd2d61a3472487c06125f3bffffffff2e17d5b8ccc0d7a4a3d009d52705be770513a47dba906eb505c8396d66df3811000000006a47304402203327261d1740dd33d0ca10a7e28ddb2862ed05dffaf81d685151e019a3e751fb0220185b9537123789b2c5200bb4f0aa098dfe6ffbc627537b6aaac5357369d4cf9c0121024276cb31dcdc70e06e6cd6e562283344e8fcf68f267dd199b3c8f140cd4d13c8ffffffff8d5929ffe66222b8cd3414a20ecfcea7d4a711100f41d762d56d825d7a786f71010000006a4730440220751c8bf1ba2d9fe5eed684d83d2083e0f083d55f338c71677e23917ee32dd06c022063e0542d41632d8e3a011fbe583a7728677e47f85cbc343441c2f111ef6c314b01210264af1414a01efb0c0381767acc16cf5f271ba49d3a3272b60520da7c95a85c2bffffffff2268b04342ecd75f79e6f14ea4c1ec11e22d7b649512f369400c17e3a860affc010000006b483045022100f5a817f1a03694d274e1c504f419c689d3e3d0823ced260dad6198dcf1b39256022042a027133f67606b349b228b29c5435dd294872d5feb122ade756e3e237a937e012103fff38371a436bbfd74b19d315d367625f38b68b2f785b53369108cf49da60f4bffffffffc23512daf04dc476a7b3b5f3ff7bbf7ae04364f31903163ad5b53602d342a4b7010000006b483045022100c74e3f77e4e7dd5f89a534612d8b09b3424094eda2ab974811285809c1e3b0b3022012f1d330b4c5b78127f2aa8bf2ea95ffe46491b5f59c17257c474ce620a72e0201210301c0b0cc55c74009051ad4f91ada8b57223cd1d56eaf87cc15363fc7c7041150ffffffffc3fba4804928ca0d22f1c74d722e817fe4011999d0dbfd5f748108011104fafd000000006b483045022100e15317e47d656da19c832af9cab8248bc1bd28fd3536227cec45b8ed28757c1b02202981cdb408577ee31d4e0c8fdc11e76bc97dd504ee9ce0299b10a605e9f58b75012103bd1b995eeba595c304d5e2ebe22ac793c1a355729e99bb0218820b6b0a284cbfffffffff8f091001be58b491b753bde74f1b3938b2674ef2f4db4c2cb509dabd392cb9bd000000006a47304402205090d866742584a66fa8663addcae8e089c9d13fb104b9e466d6ce20ed01e502022003649ec623e72e93fa7d7afafd9eeec9b8214e068011af126a5d1f4e7659b8f301210257bd210ebbe37034dd9823603ba3f6776f61c16d9b5969f465e4c256546ae453ffffffffe03387cbf249d6e15b8ff59975879e491d11b31e8ad5765392aaa544d3203197010000006b483045022100bf8874e4dbdbfc75b19e97f2e0ea5b46b9febb5f84aaf4fd4620031b9571f48d02201c60c69f476990848f1066e0ccc8e2f3dc2d90c329670c4b51debdd17494688d012103353989af6f20bab1c63ac8f87cf0365347b66ca490650154a2da8437d679bd7cffffffff023f9d6923000000001976a9144a0fe1a4b5bbe9dfbe878b64e136735d6cc083e588acc3a50f00000000001976a91409ca07592f3e5b404b9c490422f469216203f19688ac00000000'
        btcAddr = 0x4a0fe1a4b5bbe9dfbe878b64e136735d6cc083e5
        self.checkRelay(txStr, txIndex, btcAddr, hh)

        # 8 ins, 2 outs
        txIndex = 122
        txStr = '01000000013934e0623827d294bf8c99f3c3d886d92c11a8e1374157bdf09a3ec47c0ccbed010000006c493046022100d434b7d03802ee591130f2ee07c724da8cca5e67f880a23c5d44d1f551b8e5ab022100e9bb1c900a97cea0a72decc2d74cd059352885e49c7b91b22ebd764a79d780d0012102ee03e3e29926fa137dc78b15ae63b9dc9bf370065dbea04fb710eee500479117ffffffff02b0b8122a000000001976a914add23e3d2d757c9b201005fced7cbdd79a00cfe588ac60a72000000000001976a914954f0607399062d4d791b9b0b349e3817f0711b288ac00000000'
        btcAddr = 0xadd23e3d2d757c9b201005fced7cbdd79a00cfe5
        self.checkRelay(txStr, txIndex, btcAddr, hh)

        # 2 ins, 3 outs
        txIndex = 50
        txStr = '01000000015f43d26fc7ea7049a2fc63a5cd47e767ac1f8cd8bf388045e06dc5faab9e9756010000006b483045022100a51893da50d180cd3481625ce7193a43cf54b9c5ca6eedda75cef471c1afc19c022008255285e37be092ce9d793f8430cef6cc1ad12de50c56a870ee6b443f6068eb012103481e57ba7df07d0b29a827a2380f83bd349002fab509bc865c62f43e79baeb33ffffffff0356dffdfd000000001976a914c9dea40941945cf8a8955c4ee3be117d195df0f488ac20ebb304000000001976a914a9a955323f97ec609bc334fc65cc700913aa66e688acccef9201000000001976a9146f4664e7632d6e2fefc065e540eba4b71ebb371f88ac00000000'
        btcAddr = 0xc9dea40941945cf8a8955c4ee3be117d195df0f4
        self.checkRelay(txStr, txIndex, btcAddr, hh)


    def testDifficulty(self):
        self.bulkStore11FromGenesis()
        cumulDiff = self.c.getCumulativeDifficulty()
        assert cumulDiff == 11 + 1  # +1 since setInitialParent was called with imaginary block

        blockDifficulty = self.c.getAverageBlockDifficulty()
        assert blockDifficulty == 10


    def bulkStore11FromGenesis(self):
        numBlock = 11
        self.c.setInitialParent(0, 0, 1)

        strings = ""
        with open("test/headers/firstEleven.txt") as f:
            for header in f:
                strings += header[:-1]  # [:-1] to remove trailing \n

        headerBins = strings.decode('hex')
        # print('@@@ hb: ', headerBins)

        self.c.bulkStoreHeader(headerBins, numBlock)


    def bulkStore10From300K(self):
        startBlockNum = 300000
        numBlock = 10

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        strings = ""
        i = 1
        with open("test/headers/500from300k.txt") as f:
            for header in f:
                strings += header[:-1]  # [:-1] to remove trailing \n
                if i==numBlock:
                    break
                i += 1

        headerBins = strings.decode('hex')
        # print('@@@ hb: ', headerBins)

        res = self.c.bulkStoreHeader(headerBins, numBlock, profiling=True)

        print('GAS: '+str(res['gas']))
        assert res['output'] == numBlock-1 + startBlockNum

        # block 300000
        # data from pybitcointools, eg
        # >>> from bitcoin import *
        # >>> blocknum=300000
        # >>> header = get_block_header_data(blocknum)
        # >>> hashes = get_txs_in_block(blocknum)
        header = {'nonce': 222771801, 'hash': u'000000000000000082ccf8f1557c5d40b21edabb18d2d691cfbf87118bac7254', 'timestamp': 1399703554, 'merkle_root': u'915c887a2d9ec3f566a648bedcf4ed30d0988e22268cfe43ab5b0cf8638999d3', 'version': 2, 'prevhash': u'000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e', 'bits': 419465580}
        hashes = [u'b39fa6c39b99683ac8f456721b270786c627ecb246700888315991877024b983', u'7301b595279ece985f0c415e420e425451fcf7f684fcce087ba14d10ffec1121', u'6961d06e4a921834bbf729a94d7ab423b18ddd92e5ce9661b7b871d852f1db74', u'85e72c0814597ec52d2d178b7125af0e3cfa07821912ca81bf4b1fbe4b4b70f2', u'25ca9ce6e118225fd0e95febe6d835cdb95bf9e57aa2ca99ea2f140a86ca334f', u'a52997fa37fee82c0bf16638f5ec66bb0df999034c6b21bf9b8747c1abed994f', u'dd9aaf33afe6f8364a190904afcc5004fd973527be5a23f68bd7b6bd40f84c59', u'83ff2b04fe5e19f2650c5fedc706a26ab314e9edc40aed106373adaa36f6bf12', u'3c412d497cb5d83fff8270062e9fe6c1fba147eed156887081dddfcc117e854c', u'5a0ce1166ff8e6800416b1aa25f1577e233f230bd21204a6505fa6ee5a9c5fc6', u'3184aa6ccaed5f3e41fc34045970cee7501b68795c235108debd1c9a5dfec1a4', u'80bf2f098684a5db1ce0b14c0adc75efec6710a040eacfb81f64917c34e69ca5', u'80f6247937daa9ffd866e616abd337177d734a35f847669c41ec358817f3a7e8', u'3f4735eb3beb164150000b90fba6055bcff7a08ecba9352b7d29f404a658d2c9', u'c33240a15d4e252ec0284e4079776843780a7ea8836bd91f8fb8217ca23eed9b', u'15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3d5', u'60e9a2b1f7120d329fd41f1b48f5f1b3a3a581212bec241fd8f1f2a37a06efeb', u'b31214324f4c4d59540346de6cb692c02fdd31674486bff4981a8a7d8db74b6e', u'8cd58bdc6b27fd9b664e2499e9ae7d8fd8ab61757a14e9face89b1d3ce72e8d4', u'430116ff8ba9331cd0aee2530841661a9f138655eb3f013cb159d4387a5c8d75', u'07985ed09f592d6a5d87f20631f31f0e844a63eb6fdca293be5b8cdd966b5bc3', u'05cea126741dcc14e8b04a71c7b3a20790ac650a34c2af3d26ad591897a745bb', u'697699797160497048258d35a491929772d3afdb4d39e2f3b1215f69f34f95e4', u'83088c0ad83575d56013dffe44a6820d5931ec7b2df0a72a7008123714541230', u'f14255e8fa5618b03a6f99dff6c0635f565278dd951d776daa392ef8a22314cf', u'81335877f5ba07432f642206de7bb30367e3da8fa48dc91139795ecb6571e39e', u'3a87b229b9db4a9562d1453106f7b61aa67e05631cf1068cf37af910101c1b7d', u'4f4c7d7e0677f5109cc91287a7635ffb4906dc91d1287f0d8661cec0e2dcdbaa', u'0c3570cc17b033ca526fb06e3d9945aab06b279c11aee3e947a6f76b9d938cad', u'e9ce733b8397a3e39ed484e2766095e2cc3fb80e62e6c01281223d4e98516125', u'7711457b2611b68b0dd03291cbad3e56015233f7861cf087686ac8b7a6bcd2a1', u'3b4eaaa4c92e5e79f2a2b5a91517290a8134b0581cb5146b5bb34abb2da6105a', u'4d4a6f9408042e48cfd78a0151c8e01aaec829a6bd0154c9aff8020fedb19910', u'200f10f9a80042bc2ea3ce10678a22c2f2f65e8c9eb77cb02616ab994d78bc64', u'9fa29ce548cdc746ebfca93778a13f2aec7ca337b3713a508371cc895926c4e1', u'38a7fb461f35590b1b637accc0bc7cfbd8dc97cd29494f91f6de7ab650b77662', u'692229d9ddcac96288015bbbf9ef2ff21ea1f332c258ac09d67ea90a89643e1e', u'cbad0a4ee0b505a4b004e1ec9e8d845ffaab9fe006841a5de0f57f45975f638d', u'fd0fe9667036af10d633674cdd216b8f3dfe8dea8530c29735bb8494ded454d3', u'73eee43d7fd9ab2d38323a25ee776f79dd05e37e0bac5c58c3537fdf8bebb03a', u'dbb2f7d327e746cc5271f0184446319d13fdab43f7cd9c9bdb1780fb51333195', u'bb420523868848e1b60ffe28a2f5a657e7db424e11aaacca19c992eb67805349', u'd826449f965893e8a9e16e7c5eab237250167623bc2464a146bca66fa17bc859', u'a258557069b65f7376a0b183b113d09a6488998ab3b37f3b22e653064673a4f9', u'ac4e61fab92d01541734295dd8b47647989b696282d94f7e03f3d517a2c8fe0f', u'14778e8e4f139ea8d3802c9390f95d762748acd44af0bd5f990ff96254694539', u'cd127347cb166b6dc07b54e9a1212122b965116f44f64c8a181e0f1ed13a7a94', u'e9eed99ee6ad90d43fbcf01fba43c644f0d1267b7821f252ee796a29772a9da0', u'160b3ac2c0e8554a4693f618099027c183ca8528f16bca39bdf594f012e0d259', u'8d3c7ac9c640836e344dda3b2d8969d674e203cc85e1b42b364b9cd379bbc54c', u'4d493d0803f6f66755f2527c09bde9e37cf829e036f2a408c0ad40e981011808', u'ee170c8b853905e267e046da730de4efc5924b9d45a138703962bd88a427841e', u'014150195ba681ac08be9773d01cebea757139c262381b83b68505b0865df37f', u'7f3717dfb7530b2ac2f3d5891872a80616c0c9114cb813123151ef604fcec2c8', u'bac470d551be0ddcf575f6241692a059029e554b3bd759e29cb582df2c452ef1', u'f902e9c1e85fbbb970a68c54f07793b82441341cb84edfeeddbc5008dd3fa42a', u'5c42701ec8b6fa449e294c063d63a1378a82335892d8a968867e507456d6dd46', u'eec726af5ba61dfc183f23e2561af3dbc72e17567e63de8919c383aed0b34789', u'e8c8ffe8259fb98535ba4b3028b3d15726ccec383a263bfb47735d614aa1c8c5', u'79d57b6337a02b36e7fb341da626cd3f641f4393b35ad750da1f18710ec7132a', u'32e19411618c67afc97dc6ecb188d9d3a7c179ba652191f52d019a1db85eaa39', u'ef2ba16f90b39a6982df6f70600d683529d328a8b88d5f03cd9611ad2c67d898', u'313ef3fcf6a27a5cc376422e10a7a3c835aa5cce098ca206d35998f1f950907f', u'bb727c8f9cc138ec17a36355473b902f8170b415e62b537c9d9514a29b18195b', u'bd89b3e925e1a98cdfc323e27cd096f331bb8b61dce58e55277418acd4e6b81c', u'eab98223941ddf74dc5f24c50c18c94fe37de0b976ae57cf12877d2adea492c7', u'59157efb4c7ffd44d76c9e26f2aab16288d408caa821ed6840312984cab397c2', u'4a4343f87d0a15583b738447d4b252d29ec6014b364f75a6b82febdc85f77d36', u'bd2fe3c72fdff8ff934195bfbec9efde589eecc7e2486d1a27137490b934f0bb', u'5a73af81efbf315df6db9eda21e52c45462da2c2f4d9cdaa0aabaedafbe5a0c3', u'01df07dd63c90be88c2c6fdb7499f26f6af085cb9aaa71ef4a896abc7619c5e7', u'2eec110d8d89c01952cf48e71ea297c039eff7536034ebc5e6b2635d6125a636', u'93f0a25cb92a4fdde230335d8236b21309375800bfd114bad79d2b78a741b236', u'9a597af7f8cd737115368afde26fa3ddbd61f1852a30896d146b003bd96c0e28', u'6aba765dd5c019b226789bc4bcd69f27819161765d2264e231bd43afa31d5329', u'67230ecd856ea2a271d11a20e7686b8a1d8ea17b8ee39deb4999d8742619c287', u'81df42b9d145c7306aa363069bbb5dfc39f27169ba4cc0c0fe05fe957a40d5ed', u'2079d746f4ba56140cfd5ff6e8d870c7798cfa08c83984e726614ee9fe09636d', u'6eacf3862e3d96b06269971ce96e955d87e1eb036156d0f32a25dbdd83bf9ad6', u'f9a6c8c0a9d9104925b826c2f88be0e39701e2ed609a0047dff77b758427c967', u'e1822ccb952aff1d5453081116cab5dd193aa01012265153e20073b574559fc5', u'67616a53c479b20693ef82bc61b0f1d3dd6219b7b39eba3adf849666ac269d31', u'6ac0be3b5fe96e5aab1a68b073ec47ef281e4b9f1757565182a10b4d969ad979', u'c955e04d7d129735914785506fe945edcc11afdcbfff5f0c145eca5989d1ba9d', u'8bff2d6bd3371ab20b3025d017f98c7830360cdc138f8949636a375ad862ad5a', u'0c6b4796eb26bd092bc99d2f71100d15de77e9ab89d878d10940610221756e4d', u'f290713ba603832d71bd1cb055b275cbdc112bbb773079ae208adf9376ad4d8b', u'54929ba3c1b9a6a96e67a17c0ba7c63322a8852d6cba771fb8c18c6964b352d0', u'dd91af04b80457a741d0e02e4d5d9199fbca7eafc173a9db9c0c8ac39e575f4a', u'c08deba97b231b535e843a30b25ea5e82ac84b0dde44315fada98eec0e5fe0f5', u'187eb5e2503c24afbdd396c113262cfcf9a8b48ed64476f36705c9d2a14b6a1f', u'a891400adcff3db30dae2a5e6d57399c84a9467bfe5b1f8040ed3861f91413e9', u'0f771706adf8399f088489917251174402107d92bc0d28fdfdcfa48ad2b37429', u'9f12792e30797baf6a25f3128e4d89c8ffd46b667c2391a5cafeb5a8817a4118', u'd74ed5ef608c251f8ae1b06b6ca5e20ed365b96399c70a2973d03596b97ca1a8', u'6621d46781aae5ea3aea9016b517196bc8a39b4d2412dbe8ec37f148c841f992', u'b2f15a79fdb8b77966089eb53f3a7950ff5de9f0a79f0883600cc2b545b42491', u'cebe405a224b64774a9b394620c83fde847511d92145cbdc1459de2cadb93e50', u'1d2f946d69b5f48ea84dd4ed30f468126bc3d605d737d14151e7b144863e9ed6', u'dfe4429838aaff73694700a1ac2de0f18b4cc9c5c350525b0528769718a76ac2', u'd398d7ec7d847be58f32ccebb90c9a1489b51b8f02dd3ca69bd43e6695ea01ba', u'1272c9e1e3acf67ca2359076a6eb5d2ee81632ee4720b1abd18e206cf2ba58e8', u'0a8d85932d7acf42b175ce94785732db179946678f42b91bd8ea12834f5732d4', u'b0f72f99a1b8155f4e08aa5fd7b7bf1ef6a724c9f17e3b99ab3d732a66903514', u'a1be755bfc1d7bac848231bc54a0bfad250441cb0841ba5c37ef55a26ea0ffa7', u'293d0d15766fac48b94b2cf188b5bd5d53c640749f65efc747554bcc03aa6577', u'3af197c25dc773bd09b6b2f36bca282a14ddf00922a570606214bf3180bb8420', u'2ec52b1c0c312e28790a2b88014cd2bba7a8ec06902aeed321dac8b7c9098cb2', u'fabef88911c58225014d5758dd59e46916a9a122848d8c7fa8230197afc8849d', u'140d297a04eeb94a464db48da32efe7801dba32c6ecb5411c9057bb32e4f2955', u'6ec656b73c7d04e7bbc3fcefc7359c91b74040cc79fc21cfd247bef2d230f73a', u'bdae0e5dfa9f494413586dd8aca440b0bbea849a8cd9c2342ec1f27e320b971d', u'691ae0704e080e04411ebca008ce1b7ff4a05f8b67f6da2ee8aca0f32657c50e', u'e6cd0bf28ad5f512f5fdcb65b053b1662f562b3734bfc17ac952af892a767df8', u'df244e11f1bd63cc0c28073c1bb418daa8a1f7da67e6e2e7b140e2f05c8450c3', u'60ee29e4256ea0b275e6b230a531cf40f348277dd3e118948365d11cac4d9131', u'f8c9b22b2cc94966cf47e5be1c3dbc54a6e3619c08b6b957339159a504c97804', u'702451ad78d73bd3a3b3793049d6382a819750177648a0429da49b485d842173', u'45cac6176a75416c666aad603ec085e0948beae98539791a6bfec69fa5e241ac', u'0bceb62c2fe23caf701800f24e44f0278838bac015f7567f8dbfdc4d3a49d093', u'7360377a882c923bb415583777cf0b340a4fffc63350c53891564b4955976b7e', u'22d5669af43229adfcf2157de9477b013265d6fd70b1cacf7048457c65243fe4', u'c36bb17c97ebd644fc7ab9362b2d04ad63c9fae8c7f9047199c1d408df419913', u'556d7c72dd4636a5cba7fc3dedf57cb34555bf913dc09e187bdcb489c3804726', u'e48b08df0afa01a7339335fb6b6964100d11985765cbc6afcde990fd65856a9b', u'9cc064bbce74a2c56ce12b0b59fc7267a2618a35e1d8c66f642efd6d033a9681', u'12998f415cefa518a76278d82d6088d7aa512c2a1a8c3e91d826aa415c809992', u'e8b85649bdf57c0927c2f36486f1147c53ae153a2e3d6cbab1cf238d8ab65e7b', u'fafe668f8725ad2df033f3e5f86a793ac23a58283d992c1a0ff610579b56362a', u'd111d3a9bd8f499946309764effcd6bd7f1b1bb0f7f1d5562ecb88ede72bff31', u'8bec816469f65b34cc517d65b69dadc7f94fa3e19c5e34ce66351d6bd76d46b8', u'a0dbb7cf37e49483be11ce690c7c4333bd50d47df3194efcc29f141fb37e1d16', u'2855f1cf7548aad0ba6d865d9c97c95f0c7bf8dc65af38df49ad74835bc7c937', u'fa571daf7590ae943afd2b6c9072b5a47864d4e4d2055c3b4acb4ac1343c48e3', u'34d5c5fe77e6869b1b383637d058a33946dbe103edc927a0e38d26545aec8d9e', u'f87c866a8782370f004070ae1caf8b91323f1c93186a76024d439127dcd87c1a', u'2b1a908eaa8add861703d10976e64ac7946c8b83be65d66c2de4bcbac4e3cb4e', u'fea520c626ab8832451e589a4e430723a70157de7bdfbda10b61b0c618c2744f', u'1f5bbe466a99c2f75a7bc126372f56323abeaa2c2b66f972745cf153194dd71f', u'af3fcfa1440bc4d40436c69ca1d63d3bee61ffd7f41124e58a8eeac371ef9876', u'e8c5e36001052efaa2b5df0b28457002887ae73b6e49ce77f4229ad0e04a5caa', u'2865ec584fa147a52c644b744f8044502d3625e7637b55fc43f42533f3918791', u'c574cbf9ee51c461ad7b1a946760df0e996c174e331ec7c0d3ae1818d38442e2', u'f7f96a71f0e33be4665f8856b89549d46f663a1f5d5ca91efa10b0d2ee969a1a', u'ece6636a6afb756930b25915fd71940f8cb0f398348866a73cd100ddf54774e7', u'1a1ae6e74af37afbb8ed812f779cb505410f439b380d08c33832fb7291e4fa3d', u'86c7d896023f918da17cbc411110999e094b0c9434e457711eb54c56ca7b7786', u'f2f814c488de5382fcca21deabac38cc7aabdbdc9eff28131a426b9c09069e56', u'c567df44fa6c0a613394524943c2a01258da8e7f7fe532cc2bb3a2176f202c74', u'dd26818f759d5566ad3de82bfee739d138ba55e4d46315fbef4f5f4c000aa8b1', u'20cf5a1ff51f2c4ccb7e842b09238167e1951be18f409439ba7d0b074a9aa035', u'0842b84421b9f010ef4390fb70e7fd0e25a868bf3823822f168c49a0247ba552', u'62650f017ac2eb9c75a0544d992c527062823d579108545cb2a5479fb359b8a9', u'543153fff73eb3a86f7d33934889aded91626e2ddd8d6391cfd3183f94467057', u'c699b2e258c8f2659dd6288f303929485c03093b9b195b76ad2a72dc1942aff4', u'5f8ee140aa6e9458d8cc98fd04de577d9f1d5f7ba22d1aaea9dbf18d29f4aad5', u'195624d25e16e2f21477c0e944dadbd8562eb95d7d6f02a10eb9d1706ccd6be0', u'9f8a4be4106745a1c9615c24dcb33e676fc20b263b790dcc5938bd25c9cfa7b6', u'c61d7b9e7f27c88c90cb88cf5c14cd2733dfa126ca916c967b5425e13d6dbef2', u'fcc5e7327547595acec6d5496dbb7047bbd3d7bef15d8a99614507791a0e919c', u'12e58986ff3f692e1d9811d4b7504f9ab12a8328d01cb384561372a8977fcb4f', u'36bf83edfee9780bf71d5ae2e5564682c093ee856e0df242df68cf36f636cde3', u'7aa7d8dc67d83997271055fad15ba87439caca44cb887d8494e2e3d7a035489e', u'6bcc5699a9d768e7c32a7cbacecf4e04c0a3b47664435e85c267f35e62b34a40', u'464ce88d4978fd2aeb1d07b9859cf4bbc7d64835da34c8908a422cd69b05764d', u'4081f9bc98d0fe6c1be648ba58d3038f178d367033d5504826d89dc01b641883', u'8fddc291012eec652f89ec544c25a62d5c7b56485cb62aa84b4cdd1e5b9bc6e3', u'4ea733208b1287b4b6158f40631dca4aea9003cfca273593efe7c55fbc2ac93b', u'26327d0878a2e51007bc4f6f8eb731729a6ece8c0c749d0b0462b7d27ed9dec4', u'79e6e69805cf4148decdb67fb230242f176456070e989fbba170a202ae6e8be0', u'5f706df8103ee22d87715c5d766af8a965c9f3d3ab393663acecd1a88f9e5732', u'5ee987ebefa35b7a7ee95e5239fc04f5777e6b5e290c056174d87636d388d783', u'173f27313b60ead70171fbd0ab755c7d6e40d1336f1c427d34bf138615121a64', u'c29fd604274e072c2bd4a879dcfa516b5c8d278a2123bcdd58d52b9040353137', u'e4655d09893a5b5d96fc911aa73140a67f8ccdb43354522f125706e7f0a9c3f2', u'31f27a1e742f9590c4a3b2a9c6e95d44f265cb328d52cc0dcb17a133920a84b1', u'1f5dff66b173bce3eb9899a2e03525e0ce4ce26d21b311c11361df9c097bf4ab', u'94bf9d213499a3dbb6938c81f92a7584a9d74912534519f7372548477eb582e2', u'fcaa773d66d90f0509375bf9fd47fdb665b215959095b140d30ebc07435f6672', u'9b3cbace712f1fef331b91a4a557395d771c00f177f286276d8f039a4f508837', u'7cf112ba96c4999533ca3f2d27b3b7580ec90658918d10cb4f161ec35102a815', u'91fbee07653d38151b3ac628624716c7ed0822245335368b4cffdafdfddba2a4', u'8b516fc42ee3cfe729559e53df509aac06f2d2ea67b4198d75f50ba57968556f', u'fabf8e33fdcc6d874a2799d2006286f7584a9e4b6962271df7183f7f40c801fa', u'42afd1587aeaff52e62569d8ba87a26839e2c0213ace92518fd0762dd52b00e2', u'e4962898a6f3c54337f38ce9e941092748f1d16aa214fa8094b0fc7b643c6d25', u'f071a9340dcc73755a775083bb1cf50f7c4ce43afc0faeabae324c47c74b506b', u'50cf012c35ad0a5f38506fa510e81122e1db8942916c71ed3ab09ed81ec2322b', u'fa67048a1d19de38779d9a784980f1fbbc2cffac51e9cf2eb5428cf50463e173', u'7f55b1be49234705fe38c0b20b21bb8b80ebeef7caa115e59163f732c93abadf', u'141e4ea2fa3c9bf9984d03ff081d21555f8ccc7a528326cea96221ca6d476566', u'09636b32593267f1aec7cf7ac36b6a51b8ef158f5648d1d27882492b7908ca2e', u'5bf2fc8b3d5fd649104ea4a0996a263a22d9a27bb8bbf7c5620ddfa59180415d', u'bb98981ae53448e37f9f9b92308532ebbaf2cbe1cf678971b3c48f8556e3bace', u'4507c1c9eb8898e959fe563f26410f74ee898f57e799fce6d2bb3c9e7768d2e0', u'45f347c4811a168cb9a517b1a67f4c27ceeefa0d6fe92b62f4f32023282759c1', u'8b8bb1e04c132542b2e4fec124bbf1587e8206e635ada0c5bc77adc84a69d71c', u'8f05b10b8bcd0f9c646133c2a6c2b862b987d4bab1fc543e203d225f51d332f2', u'92951b259f6f50af6b0c9615b02f4cd32adaa68b44b0a1f341e51b8d066f7242', u'8c2c452e01c8e1fedcce515d8eeaeb554fb8d3a9199c8f7487b43f97dff78b24', u'b3a8743a49ebc07d51063f05cfee21e0550c88bd066ba4848d3407d3b83caa67', u'6bf1e0eaacd3a028314404fcf7070857718d9d6b1effef8ae30b1dd12daeecc0', u'4de44365c2d8cccc47146eddc30a3ce1c0f3cf2f02a76d5bc448ab9df8e9a50a', u'a7fa6bb651795f601bc5b30d46f2ebc54c1f4e64660ba3e2c9aa4ff67b5b2b44', u'0f22eceac6512674cefc616ec02e8602e39b7988335d354b4b9e46b202a4d1e6', u'076c4630f3233c40f2d081ca5205c0511e3ae151a843d07a241a367efc459d8a', u'381c90c62d292e883a9954f4cb30910a22a2ecf623f81c479e3bb62c076ae15c', u'f2b36993c8b6954a49fc8101a5a73be1c12e1dc54607e4155f6cc89050dcdc3f', u'17e92b3249912210d734ea870724e5aa89d14fdac19775c6f3fb27b0443b578f', u'df9d82e7d64773876cba3f238d3314156a9c047bea43f74b3d333e58e32c02e8', u'1f001521ff4d15c9cf5e0573b7626089f0fc3adc80f3a95efe27a5bf11d42cdc', u'fc15cc1b201179302bb865ad94157dab220200feca696db1719b6305ce438caf', u'af5a9d4881abbb86176fec8f19b70e2bec2ba331e55660c84a65ae56858f2140', u'b4fcb470c50bb9de902d78b068ff8fcbd43f2a703405f12c67c33b8f0d142333', u'7e59df63b51452499b8e8916e077e1a8b031ff2a3578fa7362d6b8847fb0b087', u'8e3c4705b993a7b62088586e8ad07d4d53dbca75cf3d7dcfaed856b0724a9e36', u'8ad2f603082827e24cabf1079e90216d5c0ad9071cf326a88625ac22fd654635', u'686ffa6fa20cb99f5b66741546e854363569d6b6557481d41947b5b4243e02a1', u'278d14dbae58d976299144c063727c0d8608b2df09d1d6f98d08dcd016db1d3f', u'f2486038276fe29dad82f1c163119b01c33638a2699ab7c0e97a6c4a1d7ecc14', u'83e276a9ab6d8936435e222d0dbd25bfce1b6a05e25d3cb311ca800aebe26cc3', u'ea81826abb33c8e2001daa1adf1d807d958cb007422cc77c1873cf302bd338b3', u'b6c73b487847f9f23716dd4aa37572d0ef33a061e5763a5277dafc1e09c0804a', u'edab80d85ad6cb79c42eb909d36031268cf801b79d70c3aa314e9485b8aeb071', u'8570dece43243e0e648edf63803c4c4a92ef2f84085db5219c2d932a80f6c68c', u'64d02bff2385b2406bcce5084cffffcf2b251ad19cf2da353a83a01eaf248907', u'ba7e4f59b925eddd31c349392ab92655e30ea41f66b90441ac190310f05f8eea', u'2f637d397e7a7f475b31d7cbac564ffc52ff7a2e826590c1a07b67c863e819dc', u'10d3aa0309d9f6ac4a58a75563ca49667965b6a9f454eef10b024b5f91eb030f', u'446249cf6bd83ee255cae174194a03e9c653648f219eed3a9d0edffd1892ce19', u'07fa53991a585d45fef3d8434a4004c56e335a936efc8fb77776481c9fdd88ea', u'9aa48344a6f4d316c0be11d3591c4a0597af167bc68208234ed479f71486a5b4', u'e0c4a881e591e1d05000443821b0c524c81236ea4248f39985635afade584166', u'75a98ce35b869772adbf643b3f8acadfa5b46b4cd8bfef26f9e079c517018285', u'e67f95cd4d5682f2b9d4e19b658baae692d669e550e6e3337c07d7395800c5a9', u'9a23b701a614b81746c0a44caa8b393844f94aaa8a13b57666a6813464e72f94', u'3b115dcc8a5d1ae060b9be8bdfc697155f6cf40f10bbfb8ab22d14306a9828cb']

        return [header, hashes]

    # this is consistent with the assumption that the ether address is the output
    # following the 'btcAddr' and that the outputs are standard scripts
    # (OP_DUP OP_HASH160 <address> OP_EQUALVERIFY OP_CHECKSIG)
    def checkRelay(self, txStr, txIndex, btcAddr, hh):
        [header, hashes] = hh
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, txIndex)


        # verify the proof and then hand the proof to the btc-eth contract, which will check
        # the tx outputs and send ether as appropriate
        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER, sender=tester.k1)
        assert BTC_ETH.setTrustedBtcRelay(self.c.address, sender=tester.k1) == 1
        assert BTC_ETH.testingonlySetBtcAddr(btcAddr, sender=tester.k1) == 1
        res = self.c.relayTx(txStr, txHash, txIndex, siblings, txBlockHash, BTC_ETH.address, profiling=True)

        indexOfBtcAddr = txStr.find(format(btcAddr, 'x'))
        ethAddrBin = txStr[indexOfBtcAddr+68:indexOfBtcAddr+108].decode('hex') # assumes ether addr is after btcAddr
        print('@@@@ ethAddrHex: '+ethAddrBin.encode('hex'))
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance
        assert res['output'] == 1  # ether was transferred

        # exchange contract is owned by tester.k1, while
        # relay contract is owned by tester.k0
        # Thus k0 is NOT allowed to reclaim ether using the same tx
        assert 0 == self.c.relayTx(txStr, txHash, txIndex, siblings, txBlockHash, BTC_ETH.address)



    # skip since OOG
    @pytest.mark.skipif(True,reason='skip')
    @slow
    # @pytest.mark.veryslow
    def testBulkStore120(self):
        startBlockNum = 300000
        numBlock = 60

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        nLoop = 2
        j = 0
        with open("test/headers/500from300k.txt") as f:
            while j < nLoop:
                i = 1
                strings = ""
                for header in f:
                    strings += header[:-1]
                    if i==numBlock:
                        break
                    i += 1

                headerBins = strings.decode('hex')  # [:-1] to remove trailing \n
                res = self.c.bulkStoreHeader(headerBins, numBlock)

                assert res == (numBlock * (j+1))

                j += 1


        # startTime = datetime.now().time()
        # endTime = datetime.now().time()
        #
        # duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        # print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        # assert res == numBlock


    # skip since OOG
    @pytest.mark.skipif(True,reason='skip')
    def testBulkStore60(self):
        startBlockNum = 300000
        numBlock = 60

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        strings = ""
        i = 1
        with open("test/headers/500from300k.txt") as f:
            for header in f:
                strings += header[:-1]
                if i==numBlock:
                    break
                i += 1

        headerBins = strings.decode('hex')  # [:-1] to remove trailing \n
        # print('@@@ hb: ', headerBins)

        startTime = datetime.now().time()
        res = self.c.bulkStoreHeader(headerBins, numBlock, profiling=True)
        endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        print('GAS: '+str(res['gas']))
        assert res['output'] == numBlock




    # we generally want to skip this since it is covered by BulkStore60
    # @pytest.mark.veryslow
    def testBulkStore5(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        # 7 here, but only storing 5 headers since OOG
        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]

        count = 5
        strings = ""
        for i in range(count):
            strings += headers[i]

        headerBins = strings.decode('hex')

        res = self.c.bulkStoreHeader(headerBins, count, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == count-1 + 100000
